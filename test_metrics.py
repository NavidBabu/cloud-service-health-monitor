import unittest
from app.metrics import Event, build_event, calculate_metrics

class MetricsTests(unittest.TestCase):
    def test_build_event(self):
        e = build_event(1, " WARNING ", " api ", 12.345, True)
        self.assertEqual(e.severity, "warning")
        self.assertEqual(e.component, "api")
        self.assertEqual(e.latency_ms, 12.35)

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            build_event(1, "bad", "api", 1, True)
        with self.assertRaises(ValueError):
            build_event(1, "info", "api", -1, True)

    def test_metrics(self):
        events = [
            Event(1,"info","api",10,True,"t1"),
            Event(2,"warning","api",30,False,"t2"),
            Event(3,"critical","db",20,True,"t3"),
        ]
        r = calculate_metrics(events)
        self.assertEqual(r["event_count"], 3)
        self.assertEqual(r["success_rate"], 0.6667)
        self.assertEqual(r["avg_latency_ms"], 20.0)
        self.assertEqual(r["components"], {"api":2,"db":1})

if __name__ == "__main__":
    unittest.main()
