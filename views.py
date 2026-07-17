import joblib
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Define file paths for the saved models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'housing_model.pkl')
MAPPING_PATH = os.path.join(BASE_DIR, 'address_mapping.pkl')

# Load the trained model and address mapping at startup
if os.path.exists(MODEL_PATH) and os.path.exists(MAPPING_PATH):
    model = joblib.load(MODEL_PATH)
    address_mapping = joblib.load(MAPPING_PATH)
else:
    model = None
    address_mapping = None

@api_view(['POST'])
def predict_price(request):
    """
    API endpoint to predict house prices based on input features.
    Accepts: Area, Room, Parking, Warehouse, Elevator, Address (text)
    """
    if model is None or address_mapping is None:
        return Response(
            {"error": "Model files not found. Please run the training script first."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        # Extract data from the POST request
        data = request.data
        area = float(data.get('Area'))
        room = int(data.get('Room'))
        parking = int(bool(data.get('Parking')))
        warehouse = int(bool(data.get('Warehouse')))
        elevator = int(bool(data.get('Elevator')))
        address = data.get('Address')

        # Convert text address to its corresponding numerical code
        address_code = address_mapping.get(address)
        if address_code is None:
            # If the address is unknown, assign a default or average code (-1)
            address_code = -1

        # Prepare features for the model
        features = [[area, room, parking, warehouse, elevator, address_code]]

        # Predict price
        predicted_price = model.predict(features)[0]

        # Return the result as JSON
        return Response({
            "status": "success",
            "predicted_price_irr": round(predicted_price, 2),
            "formatted_price": f"{round(predicted_price):,}"
        }, status=status.HTTP_200_OK)

    except (ValueError, TypeError) as e:
        return Response(
            {"error": "Invalid input data types.", "details": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": "An error occurred during prediction.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )