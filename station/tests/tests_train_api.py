from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station.models import Train, TrainType
from station.serializers import TrainListSerializer, TrainRetrieveSerializer

TRAIN_URL = reverse("station:train-list")
JOURNEY_URL = reverse("station:journey-list")


def detail_url(train_id):
    return reverse("station:train-detail", args=(train_id,))


def sample_train(**params) -> Train:
    train_type, _ = TrainType.objects.get_or_create(name="Default Type")
    defaults = {
        "name": "Test",
        "cargo_num": 10,
        "places_in_cargo": 50,
        "train_type": train_type
    }
    defaults.update(params)
    return Train.objects.create(**defaults)


class UnauthenticatedTrainApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="test"
        )
        self.client.force_authenticate(self.user)

    def test_trains_list(self) -> None:
        sample_train()

        res = self.client.get(TRAIN_URL)
        trains = Train.objects.all()
        serializer = TrainListSerializer(trains, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_trains_by_train_type(self) -> None:
        train1 = sample_train()
        train_type = TrainType.objects.create(name="TestType")
        train2 = sample_train(train_type=train_type)

        res = self.client.get(
            TRAIN_URL, {"train-type": f"{train_type.name}"}
        )
        serializer_train1 = TrainListSerializer(train1)
        serializer_train2 = TrainListSerializer(train2)

        self.assertIn(serializer_train2.data, res.data["results"])
        self.assertNotIn(serializer_train1.data, res.data["results"])

    def test_retrieve_train_detail(self) -> None:
        train = sample_train()
        url = detail_url(train.id)
        res = self.client.get(url)

        serializer = TrainRetrieveSerializer(train)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_train_forbidden(self) -> None:
        train_type = TrainType.objects.create(name="TrainType")
        payload = {
            "name": "Test",
            "cargo_num": 10,
            "places_in_cargo": 50,
            "train_type": train_type.id
        }
        res = self.client.post(TRAIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.test", password="testpassword", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_train(self) -> None:
        train_type = TrainType.objects.create(name="TrainType")
        payload = {
            "name": "Test",
            "cargo_num": 10,
            "places_in_cargo": 50,
            "train_type": train_type.id
        }
        res = self.client.post(TRAIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
