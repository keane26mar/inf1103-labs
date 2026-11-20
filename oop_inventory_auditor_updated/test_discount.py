import unittest
from discount import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

class TestDiscountStrategies(unittest.TestCase):
    
    def test_no_discount(self):
        try:
            strategy = NoDiscount()
            result = strategy.apply(150.0)
            self.assertEqual(result, 150.0)
            print("SUCCESS: test_no_discount passed (Total remained 150.0)")
        except AssertionError as e:
            print(f"ERROR: test_no_discount failed! {e}")
            raise

    def test_percentage_discount(self):
        try:
            strategy = PercentageDiscount(10.0)
            result = strategy.apply(200.0)
            self.assertEqual(result, 180.0)
            print("SUCCESS: test_percentage_discount passed (200.0 with 10% off is 180.0)")
        except AssertionError as e:
            print(f"ERROR: test_percentage_discount failed! {e}")
            raise

    def test_bulk_discount_meets_threshold(self):
        try:
            strategy = BulkDiscount(threshold=200.0, discount_amount=20.0)
            result = strategy.apply(250.0)
            self.assertEqual(result, 230.0)
            print("SUCCESS: test_bulk_discount_meets_threshold passed (250.0 met threshold, $20 off is 230.0)")
        except AssertionError as e:
            print(f"ERROR: test_bulk_discount_meets_threshold failed! {e}")
            raise

    def test_bulk_discount_below_threshold(self):
        try:
            strategy = BulkDiscount(threshold=200.0, discount_amount=20.0)
            result = strategy.apply(150.0)
            self.assertEqual(result, 150.0)
            print("SUCCESS: test_bulk_discount_below_threshold passed (150.0 below threshold, no discount)")
        except AssertionError as e:
            print(f"ERROR: test_bulk_discount_below_threshold failed! {e}")
            raise

    def test_student_discount(self):
        try:
            strategy = StudentDiscount(15.0)
            result = strategy.apply(100.0)
            self.assertEqual(result, 85.0)
            print("SUCCESS: test_student_discount passed (100.0 with 15% off is 85.0)")
        except AssertionError as e:
            print(f"ERROR: test_student_discount failed! {e}")
            raise

if __name__ == "__main__":
    unittest.main()