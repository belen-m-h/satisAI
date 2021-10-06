import datetime
import unittest

from Cooking.Cooking import checkCookingAvailability


order_time = datetime.datetime(2020, 12, 8, 19, 16, 5)
order_time = "2020-12-8 19:16:05"

cooking_slots = {
    0: datetime.datetime(2020, 12, 8, 19, 20, 31),
    1: datetime.datetime(2020, 12, 8, 19, 20, 31),
    2: datetime.datetime(2020, 12, 8, 19, 19, 31),
    3: datetime.datetime(2020, 12, 8, 19, 19, 32)
}

assembling_slots = {
    0: datetime.datetime(2020, 12, 8, 19, 28, 31),
    1: datetime.datetime(2020, 12, 8, 19, 28, 31),
    2: datetime.datetime(2020, 12, 8, 19, 28, 31)
}

packaging_slots = {
    0: datetime.datetime(2020, 12, 8, 19, 30, 31),
    1: datetime.datetime(2020, 12, 8, 19, 29, 31)
}

cooking_t = 1
assembling_t = 2
packaging_t = 1

bugers_dict_on_time = {
    0: {'order_time': None, 'step_finish_time': None, 'step': None},
    1: {'order_time': None, 'step_finish_time': None, 'step': None},
    2: {'order_time': None, 'step_finish_time': None, 'step': None},
    3: {'order_time': None, 'step_finish_time': None, 'step': None},
    4: {'order_time': None, 'step_finish_time': None, 'step': None}
}

bugers_dict_not_on_time = {
    0: {'order_time': None, 'step_finish_time': None, 'step': None},
    1: {'order_time': None, 'step_finish_time': None, 'step': None},
    2: {'order_time': None, 'step_finish_time': None, 'step': None},
    3: {'order_time': None, 'step_finish_time': None, 'step': None},
    4: {'order_time': None, 'step_finish_time': None, 'step': None},
    5: {'order_time': None, 'step_finish_time': None, 'step': None},
    6: {'order_time': None, 'step_finish_time': None, 'step': None},
    7: {'order_time': None, 'step_finish_time': None, 'step': None},
    8: {'order_time': None, 'step_finish_time': None, 'step': None},
    9: {'order_time': None, 'step_finish_time': None, 'step': None},
}

cooking_slots_expected = {
    0: datetime.datetime(2020, 12, 8, 19, 21, 31), 1: datetime.datetime(2020, 12, 8, 19, 21, 31),
    2: datetime.datetime(2020, 12, 8, 19, 21, 31), 3: datetime.datetime(2020, 12, 8, 19, 20, 32)
}

assembling_slots_expected = {
    0: datetime.datetime(2020, 12, 8, 19, 32, 31),
    1: datetime.datetime(2020, 12, 8, 19, 32, 31),
    2: datetime.datetime(2020, 12, 8, 19, 30, 31)
}

packaging_slots_expected = {
    0: datetime.datetime(2020, 12, 8, 19, 33, 31),
    1: datetime.datetime(2020, 12, 8, 19, 33, 31)

}

burgers_dict_expected = {
    0: {'order_time': None, 'step_finish_time': datetime.datetime(2020, 12, 8, 19, 31, 31), 'step': 'PACKAGING'},
    1: {'order_time': None, 'step_finish_time': datetime.datetime(2020, 12, 8, 19, 31, 31), 'step': 'PACKAGING'},
    2: {'order_time': None, 'step_finish_time': datetime.datetime(2020, 12, 8, 19, 32, 31), 'step': 'PACKAGING'},
    3: {'order_time': None, 'step_finish_time': datetime.datetime(2020, 12, 8, 19, 33, 31), 'step': 'PACKAGING'},
    4: {'order_time': None, 'step_finish_time': datetime.datetime(2020, 12, 8, 19, 33, 31), 'step': 'PACKAGING'}
}

t_max_expected = 17


class TestName(unittest.TestCase):

    def test_check_on_time_answer(self):

        onTime, [cookingPlaces_tmp, assemblyPlaces_tmp, packagingPlaces_tmp], burgersdict_tmp, max_t_tmp =\
            checkCookingAvailability(
                order_time, cooking_slots.copy(), assembling_slots.copy(),
                packaging_slots.copy(), cooking_t, assembling_t, packaging_t, bugers_dict_on_time
            )

        self.assertEqual(onTime, True)
        assert cookingPlaces_tmp == cooking_slots_expected
        assert assemblyPlaces_tmp == assembling_slots_expected
        assert packagingPlaces_tmp == packaging_slots_expected
        assert burgersdict_tmp == burgers_dict_expected
        assert max_t_tmp == t_max_expected

    def test_check_not_on_time_answer(self):

        onTime, [cookingPlaces_tmp, assemblyPlaces_tmp, packagingPlaces_tmp], burgersdict_tmp, max_t_tmp =\
            checkCookingAvailability(
                order_time, cooking_slots.copy(), assembling_slots.copy(),
                packaging_slots.copy(), cooking_t, assembling_t, packaging_t, bugers_dict_not_on_time
            )

        self.assertEqual(onTime, False)
        assert cookingPlaces_tmp is None
        assert assemblyPlaces_tmp is None
        assert packagingPlaces_tmp is None
        assert burgersdict_tmp is None
        assert max_t_tmp is None
