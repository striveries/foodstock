from django.test import TestCase, Client

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/main/')
        self.assertTemplateUsed(response, 'main.html')
        # untuk mengecek apakah template ditemukan dan berhasil digunakan

    def test_main_response(self):
        # mengirim request ke main app
        response = Client().get('/main/')

        # mengecek apakah template sudah sesuai
        self.assertTemplateUsed(response, 'main.html')

        # mengecek apakah data yang ditampilkan sudah sesuai
        self.assertEqual(response.context['name'], 'Calista Sekar')
        self.assertEqual(response.context['class'], 'PBP C')
        self.assertEqual(response.context['item_name'], 'wortel')
        self.assertEqual(response.context['amount'], '2')