import os
import re
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.core.management.base import BaseCommand, CommandError
from apps.dreams.models import Dream
from apps.users.models import User
from apps.artefacts.models import Artefact



class Command(BaseCommand):
    help = 'Import dreams transcripts from the corpus (https://github.com/dheavy/outrenuit-corpus/)'
    MARKER_INTERPRETATION = '\n-----\n'
    MARKER_NOTES = '\n---\n'

    def add_arguments(self, parser):
        parser.add_argument(
            'path_to_files',
            help='Path to the transcript (.txt) directory of files'
        )

    def handle(self, *args, **options):
        path = options['path_to_files']
        for label in os.listdir(path):
            transcript_file = os.path.join(path, label)
            if self.is_transcript(transcript_file):
                # self.log('Reading transcript {label}'.format(label=label))
                dream_data = self.get_dream_data(label, transcript_file)
                slips = self.get_slips_data(dream_data['body'])
                if slips:
                    print(slips)
                related = self.get_related_data(dream_data['body'])
                dream = Dream(
                    body=dream_data['body'],
                    user=dream_data['user'],
                    transcripted_at=dream_data['transcripted_at'],
                    label=label
                )

    def log(self, msg):
        return self.stdout.write(msg)

    def get_dream_data(self, label, transcript_file):
        type = Dream.Typology.SLEEP
        user = self.get_user('hello@davybraun.com')
        body = self.read_transcript(transcript_file)
        transcripted_at = self.get_transcription_date(label)
        return {
            'type': type,
            'user': user,
            'body': body,
            'transcripted_at': transcripted_at
        }

    def get_slips_data(self, txt):
        if '[]' in txt:
            txt = txt.replace('[]', '[ ]')
        # slips = re.findall('\[([^\]\[]+)\]\(([^\)]+)\)', txt)
        # return bool(slips) and slips or None
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
        related_data = {}
        if self.MARKER_INTERPRETATION in txt:
            related_data['interpretation'] = self.extract_related_data(
                txt, self.MARKER_INTERPRETATION
            )
        if self.MARKER_NOTES in txt:
            related_data['notes'] = self.extract_related_data(
                txt, self.MARKER_NOTES
            )
        if bool(related_data) is False:
            return None
        return related_data

    def extract_related_data(self, txt, marker):
        return txt[txt.find(marker) + len(marker):].strip()

    def is_transcript(self, filepath):
        return os.path.isfile(filepath) and filepath[-4:] == '.txt'

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
