import os
import re
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.core.management.base import BaseCommand, CommandError
from apps.dreams.models import Dream
from apps.users.models import User
from apps.artefacts.models import Artefact
from apps.interpretations.models import Interpretation


class MissingDreamException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Command(BaseCommand):
    help = 'Import dreams transcripts from the corpus (https://github.com/dheavy/outrenuit-corpus/)'
    silent = False
    MARKER_INTERPRETATION = '\n-----\n'
    MARKER_OBSERVATIONS = '\n---\n'

    def add_arguments(self, parser):
        parser.add_argument(
            'path_to_files',
            help='Path to the transcript (.txt) directory of files'
        )

        parser.add_argument(
            '--silent',
            help='Silences logger'
        )

    def handle(self, *args, **options):
        path = options['path_to_files']
        self.silent = options['silent'] == 'True'
        files = os.listdir(path)
        files.sort()
        [self.process(os.path.join(path, f), f) for f in files if self.is_transcript(f)]

    def process(self, transcript_file, label):
        assert os.path.isfile(transcript_file)
        dream_data = self.get_dream_data(label, transcript_file)
        freudian_slips = self.get_slips_data(dream_data['body'])
        interpretation, observations = self.get_related_data(
            dream_data['body']
        )
        self.update_or_create_models(
            dream=dream_data,
            slips=freudian_slips,
            observations=observations,
            interpretation=interpretation
        )

    def log(self, label, info):
        if not self.silent:
            return self.stdout.write(self.style.SUCCESS(label) + ' ' + info)

    def update_or_create_models(self, *args, **kwargs):
        dream_data = kwargs.get('dream', None)
        if dream_data is None:
            raise MissingDreamException()
        dream, created = Dream.objects.update_or_create(
            body=dream_data['body'],
            user=dream_data['user'],
            type=dream_data['type'],
            label=dream_data['label'],
            transcripted_at=dream_data['transcripted_at'],
        )
        if created:
            self.log('--> CREATED DREAM', '(label: "{label}", "ex: {ex}")'.format(
                label=dream.label,
                ex=self.excerpt(dream.body)
            ))
        else:
            self.log('--> UPDATED DREAM', '(label: "{label}", "ex: {ex}")'.format(
                label=dream.label,
                ex=self.excerpt(dream.body)
            ))

        slips = kwargs.get('slips', None)
        if slips:
            for slip in slips:
                label_start, label_end = slip['span']
                freudian, created = Artefact.objects.update_or_create(
                    type=Artefact.Typology.FREUDIAN_SLIP,
                    label=slip['label'],
                    label_start=label_start,
                    label_end=label_end,
                    body=slip['body'],
                    dream=dream
                )
                if created:
                    self.log(
                        '----> CREATED ARTEFACT', '(Freudian slip, label: "{label}", "ex: {ex}")'.format(
                            label=freudian.label,
                            ex=self.excerpt(freudian.body)
                        )
                    )
                else:
                    self.log(
                        '----> UPDATED ARTEFACT', '(Freudian slip, label: "{label}", "ex: {ex}")'.format(
                            label=freudian.label,
                            ex=self.excerpt(freudian.body)
                        )
                    )
        observation = kwargs.get('observation', None)
        if observation:
            obs, created = Artefact.objects.update_or_create(
                type=Artefact.Typology.OBSERVATION,
                body=observation,
                dream=dream
            )

            if created:
                self.log(
                    '----> CREATED OBSERVATION',  '(dream ID: {id}, excerpt: {ex})'.format(
                        id=dream.id,
                        ex=self.excerpt(obs)
                    )
                )
            else:
                self.log(
                    '----> UPDATED OBSERVATION',  '(dream ID: {id}, excerpt: {ex})'.format(
                        id=dream.id,
                        ex=self.excerpt(obs)
                    )
                )

        interpretation = kwargs.get('interpretation', None)
        if interpretation:
            interp, created = Interpretation.objects.update_or_create(
                dream=dream,
                body=interpretation
            )
            if created:
                self.log(
                    '----> CREATED INTERPRETATION', '(dream ID: {id})'.format(
                        id=dream.id,
                        ex=self.excerpt(interp.body)
                    )
                )
            else:
                self.log(
                    '----> UPDATED INTERPRETATION', '(dream ID: {id})'.format(
                        id=dream.id,
                        ex=self.excerpt(interp.body)
                    )
                )

    def get_dream_data(self, label, transcript_file):
        type = Dream.Typology.SLEEP
        user = self.get_user('hello@davybraun.com')
        body = self.read_transcript(transcript_file)
        transcripted_at = self.get_transcription_date(label)
        return {
            'type': type,
            'user': user,
            'body': body,
            'label': label,
            'transcripted_at': transcripted_at
        }

    def get_slips_data(self, txt):
        if '[]' in txt:
            txt = txt.replace('[]', '[ ]')
        slips = []
        for match in re.finditer('\[([^\]\[]+)\]\(([^\)]+)\)', txt):
            group = match.group()
            slips.append({
                'span': match.span(),
                'label': group[1:group.find(']')],
                'body': group[group.find('(') + 1:group.find(')')]
            })
        return slips

    def get_related_data(self, txt):
        interpretation = None
        observations = None
        if self.MARKER_INTERPRETATION in txt:
            interpretation = self.extract_related_data(
                txt, self.MARKER_INTERPRETATION
            )
        if self.MARKER_OBSERVATIONS in txt:
            observations = self.extract_related_data(
                txt, self.MARKER_OBSERVATIONS
            )
        return interpretation, observations

    def extract_related_data(self, txt, marker):
        return txt[txt.find(marker) + len(marker):].strip()

    def is_transcript(self, filepath):
        return filepath[-4:] == '.txt'

    def read_transcript(self, transcript_file):
        with open(transcript_file) as f:
            body = f.read()
        return body

    def get_transcription_date(self, label):
        timestamp = label[:10]
        tz = get_current_timezone()
        dt = tz.localize(datetime.strptime(timestamp, '%Y-%m-%d'))
        return dt

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(
                'User with email {email} was not found'.format(email=email)
            )

    def excerpt(self, str, length=45):
        return str.replace('\n', '')[:length] + '...'
