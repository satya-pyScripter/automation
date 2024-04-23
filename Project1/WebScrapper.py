from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from formfiller import FormFiller

app = Flask(__name__)
api = Api(app, version='1.0', title='Web Scrapper', description='Web Scrapper')

response_model = api.model('Response', {
    'message': fields.String(description='API response message')
})

input_model = api.model('Input', {
    'data': fields.Raw(required=True, description='Input JSON data')
})

@api.route('/webscrapper')
class CallApiWithToken(Resource):
    @api.expect(input_model)
    @api.response(200, 'Successful operation', response_model)
    @api.response(400, 'Bad request')
    @api.response(500, 'Internal server error')
    def post(self):
        """
        Call API with JSON input
        """
        form_filler = FormFiller()
        try:
            # Parse JSON input
            data = request.get_json()

            # Validate JSON input
            if not data:
                return {'error': 'No JSON input provided'}, 400

            # Process input
            input_data = data.get('data')

            # Example processing (printing)
            print("Received JSON input:")
            print(input_data)
            locator_value_mapper = {
                "ZipCode": '//*[@id="zip"]',
                "selected_service": '//*[@id="serviceSelect"]',
                "Get_Free_Quotes": '(//button[@id="bg-row-button" and @onclick="redirectToPage()"])[1]',
                "monthly_bill": '//*[@id="electricity-bill"]',
                "home_owner": '//*[@id="home-owner"]',
                "next": '//*[@id="form-page-2"]'
            }

            locator_type_mapper = {
                "ZipCode": 'input_field',
                "selected_service": 'dropdown',
                "Get_Free_Quotes": 'button_element',
                "monthly_bill": 'dropdown',
                "home_owner": 'dropdown',
                "next": 'button_element'
            }

            form_filler.fill_form_page1(input_data, locator_value_mapper,locator_type_mapper,"https://ehomequote.co/")

            # Return a response
            return input_data, 200
        except Exception as e:
            # Handle exceptions
            return  str(e), 500

if __name__ == "__main__":
    app.run(debug=True)
