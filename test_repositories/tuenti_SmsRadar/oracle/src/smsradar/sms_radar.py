"""Port of com.tuenti.smsradar.SmsRadar."""


class SmsRadar(object):
    smsListener = None

    @staticmethod
    def initializeSmsRadarService(context, sms_listener):
        from .sms_radar_service import SmsRadarService
        SmsRadar.smsListener = sms_listener
        context.startService(SmsRadarService)

    @staticmethod
    def stopSmsRadarService(context):
        from .sms_radar_service import SmsRadarService
        SmsRadar.smsListener = None
        context.stopService(SmsRadarService)
