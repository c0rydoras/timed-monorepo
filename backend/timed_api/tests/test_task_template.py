from timed.jsonapi_test_case  import JSONAPITestCase
from django.core.urlresolvers import reverse
from timed_api.factories      import TaskTemplateFactory
from rest_framework           import status


class TaskTemplateTests(JSONAPITestCase):

    def setUp(self):
        super().setUp()

        self.task_templates = TaskTemplateFactory.create_batch(5)

    def test_task_template_list(self):
        url = reverse('task-template-list')

        noauth_res = self.noauth_client.get(url)
        user_res   = self.client.get(url)
        admin_res  = self.admin_client.get(url)

        self.assertEqual(noauth_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(user_res.status_code,   status.HTTP_200_OK)
        self.assertEqual(admin_res.status_code,  status.HTTP_200_OK)

        result = self.result(admin_res)

        self.assertEqual(len(result['data']), len(self.task_templates))

        self.assertIn('id',   result['data'][0])
        self.assertIn('name', result['data'][0]['attributes'])

    def test_task_template_detail(self):
        task_template = self.task_templates[0]

        url = reverse('task-template-detail', args=[
            task_template.id
        ])

        noauth_res = self.noauth_client.get(url)
        user_res   = self.client.get(url)
        admin_res  = self.admin_client.get(url)

        self.assertEqual(noauth_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(user_res.status_code,   status.HTTP_200_OK)
        self.assertEqual(admin_res.status_code,  status.HTTP_200_OK)

        result = self.result(admin_res)

        self.assertIn('id',   result['data'])
        self.assertIn('name', result['data']['attributes'])

    def test_task_template_create(self):
        data = {
            'data': {
                'type': 'task-templates',
                'id': None,
                'attributes': {
                    'name': 'Test Task Template'
                }
            }
        }

        url = reverse('task-template-list')

        noauth_res = self.noauth_client.post(url, data)
        user_res   = self.client.post(url, data)
        admin_res  = self.admin_client.post(url, data)

        self.assertEqual(noauth_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(user_res.status_code,   status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_res.status_code,  status.HTTP_201_CREATED)

        result = self.result(admin_res)

        self.assertIsNotNone(result['data']['id'])

        self.assertEqual(
            result['data']['attributes']['name'],
            data['data']['attributes']['name']
        )

    def test_task_template_update(self):
        task_template = self.task_templates[0]

        data = {
            'data': {
                'type': 'task-templates',
                'id': task_template.id,
                'attributes': {
                    'name': 'Test Task Template'
                }
            }
        }

        url = reverse('task-template-detail', args=[
            task_template.id
        ])

        noauth_res = self.noauth_client.patch(url, data)
        user_res   = self.client.patch(url, data)
        admin_res  = self.admin_client.patch(url, data)

        self.assertEqual(noauth_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(user_res.status_code,   status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_res.status_code,  status.HTTP_200_OK)

        result = self.result(admin_res)

        self.assertEqual(
            result['data']['attributes']['name'],
            data['data']['attributes']['name']
        )

    def test_task_template_delete(self):
        task_template = self.task_templates[0]

        url = reverse('task-template-detail', args=[
            task_template.id
        ])

        noauth_res = self.noauth_client.delete(url)
        user_res   = self.client.delete(url)
        admin_res  = self.admin_client.delete(url)

        self.assertEqual(noauth_res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(user_res.status_code,   status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_res.status_code,  status.HTTP_204_NO_CONTENT)
