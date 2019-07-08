default_data = {
  'meta': {
    'LenderCode': "bankb",
    'TransactionId': "KpSz_NBS10Zi2e9SoXGntiFd",
    'TransactionType': "EstimatePayment",
    'LenderReferenceNumber': "96598214"
  },
  'data': {
    'StatusCode': "pre-approved",
    'StatusMessage': "Bank returned the estimate payment",
    'IssuedOn': "2019-07-10T10:50:32.2494116-04:00",
    'EstimatePaymentRequest': {},
    'PaymentOptions': [{
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
         }]
  },
  'errors': [{
      'InternalCode': "abc123",
      'Severity': "validation_error",
      'Detail': "Description for the error..."
    }]
}

from flask import Blueprint, jsonify, request
simulation_app = Blueprint('simulation_app', __name__, template_folder='templates')

@simulation_app.route('/simulation', methods=['POST'])
def simulate():
    body_from_request = request.get_json()
    default_data['data']['EstimatePaymentRequest'] = body_from_request
    return jsonify(default_data)