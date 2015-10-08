from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.exceptions import ObjectDoesNotExist
from authentication.models import Account
from posts.models import Post
from django.core.urlresolvers import reverse

# Create your tests here.
class FileUploadTests(APITestCase):

    def setUp(self):
        self.tearDown()
        u = Account.objects.create_user('test', username='test', password='test'#,email='test@test.test'
        	)
        u.save()

    def tearDown(self):
        try:
            u = Account.objects.get_by_natural_key('test')
            u.delete()

        except ObjectDoesNotExist:
            pass
        Post.objects.all().delete()

    def _create_test_file(self, path):
        f = open(path, 'w')
        f.write('test123\n')
        f.close()
        f = open(path, 'rb')
        return {'datafile': f}

    def test_upload_file(self):
        url = '/tmp/'
        data = self._create_test_file('/tmp/test_upload')

        # assert authenticated user can upload file
        token = Account.objects.get(username='test')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)
        self.assertTrue(urlparse(
            response.data['datafile']).path.startswith(settings.MEDIA_URL))
        self.assertEqual(response.data['owner'],
                       User.objects.get_by_natural_key('test').id)
        self.assertIn('created', response.data)

        # assert unauthenticated user can not upload file
        client.logout()
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)