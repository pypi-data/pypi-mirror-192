from aus.proto.orchestration.message_pb2 import AusFeature, BytesList, Int64List, FloatList, AusFeatures
from aus.proto.orchestration.data_pb2 import Example


def create_bytes_data(value):
    """Returns a bytes_list from a string / byte."""
    return AusFeature(bytes_list=BytesList(value=[value]))


def create_float_data(value):
    """Returns a float_list from a float / double."""
    return AusFeature(float_list=FloatList(value=[value]))


def create_int64_data(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return AusFeature(int64_list=Int64List(value=[value]))


if __name__ == '__main__':
    # examples

    # print(create_bytes_data(b'test_string'))
    # print(create_bytes_data(u'test_bytes'.encode('utf-8')))
    # print(create_float_data(3.14))
    # print(create_int64_data(34))
    # print(create_int64_data(True))
    # print(create_int64_data(False))

    # serialize to string
    # my_message = create_float_data(3.14)
    # print(my_message.SerializeToString())

    # Data
    # Create a dictionary mapping the feature name to the tf.train.Example-compatible # data type.
    my_apis = {
        'Archive.org': create_bytes_data(b'https://archive.org/metadata/TheAdventuresOfTomSawyer_201303'),
        'binance.com': create_bytes_data(b'https://data.binance.com/api/v3/ticker/24hr')
    }
    send_data = Example(features=AusFeatures(feature=my_apis))
    # print(dir(send_data))

    data = send_data.SerializeToString()
    print(data)


