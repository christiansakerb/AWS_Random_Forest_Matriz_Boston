import math
import numpy 
from model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    print('holaa')
    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, list)
    print('Se evalua que sea una lista')
    assert len(predictions)==5
    print('Muy bien se imprimien todas las predicciones')
    print(predictions[0])
    #assert isinstance(predictions[0], numpy.floating)
    assert result.get("errors") is None
