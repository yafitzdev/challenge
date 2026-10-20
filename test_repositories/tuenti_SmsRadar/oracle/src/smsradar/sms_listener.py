"""Port of com.tuenti.smsradar.SmsListener."""


class SmsListener(object):
    """Listener notified when an SMS is sent or received."""

    def onSmsSent(self, sms):
        raise NotImplementedError

    def onSmsReceived(self, sms):
        raise NotImplementedError
