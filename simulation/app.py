default_data = {
  'meta': {
    'LenderCode': "Sirimulation Bank",
    'TransactionId': "9999",
    'TransactionType': "EstimatePayment",
    'LenderReferenceNumber': "1234"
  },
  'data': {
    'StatusCode': "pre-approved",
    'StatusMessage': "Bank returned the estimate payment",
    'IssuedOn': "2019-07-10T10:50:32.2494116-04:00",
    'EstimatePaymentRequest': {},
    'PaymentOptions': {
          'Term': 48,
          'Interest': 16,
          'VehicleInstallmentValue': 2000.00,
          'FinanceInsuranceInstallmentValue': 4000.67,
          'IOFValue': 450.00,
          'IOFValueWithInsurance': 500.99,
          'InsuranceValue': 50.00,
          'ContractRecordRate': 15,
          'PropertyValuatiuonRate': 3.9,
          'CustomerRegistrationFee': 100.00
         }
  },
  'errors': [{
      'InternalCode': "abc123",
      'Severity': "validation_error",
      'Detail': "Description for the error..."
    }]
}

import re
from flask import Blueprint, jsonify, request

simulation_app = Blueprint('simulation_app', __name__, template_folder='templates')
from app import find_vehicle_match_short

def calculate_payment_options(selling_price, downpayment, terms):
    customer_reg_fee = 100
    return {
        'Term': terms,
        'Interest': 1,
        'VehicleInstallmentValue': (((selling_price + customer_reg_fee) - downpayment) / terms),
        'FinanceInsuranceInstallmentValue': 0,
        'IOFValue': 0,
        'IOFValueWithInsurance': 0,
        'InsuranceValue': 0,
        'ContractRecordRate': 1,
        'PropertyValuatiuonRate': 0,
        'CustomerRegistrationFee': customer_reg_fee
    }

@simulation_app.route('/simulation', methods=['POST'])
def simulate():
    body_from_request = request.get_json()
    data = body_from_request['data']
    financing_terms = data['FinancingTerms']
    vehicle = data['Vehicle']
    extracted_vehicle = vehicle['Trim']

    selling_price = float(re.sub(r'[^\d|.]', '', str(vehicle['SellingPrice'])))
    downpayment = float(re.sub(r'[^\d|.]', '', str(financing_terms['DownPayment'])))
    terms = int(re.sub(r'[^\d|.]', '', str(financing_terms['Term'])))

    payment_options = calculate_payment_options(selling_price, downpayment, terms)
    json_vehicle_data = find_vehicle_match_short(extracted_vehicle)
    default_data['data']['EstimatePaymentRequest'] = body_from_request
    default_data['data']['PaymentOptions'] = payment_options

    default_data['data']['Vehicle'] = json_vehicle_data.get_json()
    return jsonify(default_data)