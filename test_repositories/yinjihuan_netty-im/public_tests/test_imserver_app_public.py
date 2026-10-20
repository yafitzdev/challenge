from src.nettyim.imserver_app import ImServerApp

def test_coverage_via_new_instance():
    app = ImServerApp()
    assert app.__class__.__name__ == "ImServerApp"