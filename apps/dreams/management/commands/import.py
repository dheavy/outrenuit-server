import os
import re
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.core.management.base import BaseCommand, CommandError
from apps.dreams.models import Dream
from apps.users.models import User
from apps.interpretations.models import Interpretation
from apps.artefacts.models import FreudianSlip, Observation


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
        freudian_slips = self.get_slips_data(dream_data['text'])
        interpretation, observations = self.get_related_data(dream_data['text'])
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
            text=dream_data['text'],
            user=dream_data['user'],
            type=dream_data['type'],
            title=dream_data['title'],
            transcripted_at=dream_data['transcripted_at'],
        )
        if created:
            self.log('--> CREATED DREAM', '(title: "{title}", "text: {ex}")'.format(
                title=dream.title,
                ex=dream.excerpt(dream.text)
            ))
        else:
            self.log('--> UPDATED DREAM', '(title: "{text}", "text: {ex}")'.format(
                title=dream.title,
                ex=dream.excerpt(dream.text)
            ))

        slips = kwargs.get('slips', None)
        if slips:
            for slip in slips:
                snippet_start, snippet_end = slip['span']
                freudian, created = FreudianSlip.objects.update_or_create(
                    dream=dream,
                    meant=slip['meant'],
                    slipped=slip['slipped'],
                    snippet_start=snippet_start,
                    snippet_end=snippet_end
                )
                if created:
                    self.log(
                        '----> CREATED ARTEFACT', '(Freudian slip, slipped: "{slipped}", "meant: {meant}")'.format(
                            slipped=freudian.slipped,
                            meant=freudian.meant
                        )
                    )
                else:
                    self.log(
                        '----> UPDATED ARTEFACT', '(Freudian slip, slipped: "{slipped}", "meant: {meant}")'.format(
                            slipped=freudian.slipped,
                            meant=freudian.meant
                        )
                    )
        observation = kwargs.get('observation', None)
        if observation:
            obs, created = Observation.objects.update_or_create(
                text=observation,
                dream=dream
            )

            if created:
                self.log(
                    '----> CREATED OBSERVATION', '(dream: {dream}, text: {text})'.format(
                        dream=bool(dream.title) and dream.title or dream.id,
                        ex=obs.excerpt(obs.text)
                    )
                )
            else:
                self.log(
                    '----> UPDATED OBSERVATION', '(dream: {dream}, text: {text})'.format(
                        dream=bool(dream.title) and dream.title or dream.id,
                        ex=obs.excerpt(obs.text)
                    )
                )

        interpretation = kwargs.get('interpretation', None)
        if interpretation:
            interp, created = Interpretation.objects.update_or_create(
                dream=dream,
                text=interpretation
            )
            if created:
                self.log(
                    '----> CREATED INTERPRETATION', '(dream: {dream}, text: {text})'.format(
                        dream=bool(dream.title),
                        text=self.excerpt(interp.text)
                    )
                )
            else:
                self.log(
                    '----> UPDATED INTERPRETATION', '(dream: {dream}, text: {text})'.format(
                        dream=bool(dream.title),
                        text=self.excerpt(interp.text)
                    )
                )

    def get_dream_data(self, label, transcript_file):
        type = Dream.Typology.SLEEP
        user = self.get_user('hello@davybraun.com')
        text = self.read_transcript(transcript_file)
        transcripted_at = self.get_transcription_date(label)
        return {
            'type': type,
            'user': user,
            'text': text,
            'title': label,
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
                'slipped': group[1:group.find(']')],
                'meant': group[group.find('(') + 1:group.find(')')]
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

    def excerpt(self, string, length=45):
        return string.replace('\n', '')[:length] + '...'
