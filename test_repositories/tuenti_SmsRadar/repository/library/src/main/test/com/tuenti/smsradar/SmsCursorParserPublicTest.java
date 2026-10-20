package com.tuenti.smsradar;

import org.junit.Assert;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

public class SmsCursorParserPublicTest {

    @Test
    public void testParseSingleSmsRow() {
        List<String[]> rows = new ArrayList<>();
        rows.add(new String[]{"+3450000000", "Text from Eve", "Eve", "1600000000000", "3"});
        List<Sms> smses = SmsCursorParser.parse(rows);
        Assert.assertEquals(1, smses.size());
        Sms sms = smses.get(0);
        Assert.assertEquals("+3450000000", sms.getAddress());
        Assert.assertEquals("Text from Eve", sms.getMessage());
        Assert.assertEquals("Eve", sms.getContact());
        Assert.assertEquals(1600000000000L, sms.getTime());
        Assert.assertEquals(SmsType.DRAFT, sms.getType());
    }

    @Test
    public void testParseMultipleSmsRows() {
        List<String[]> rows = new ArrayList<>();
        rows.add(new String[]{"123", "Bulk1", "A", "1600001", "1"});
        rows.add(new String[]{"456", "Bulk2", "B", "1600002", "2"});
        List<Sms> smses = SmsCursorParser.parse(rows);
        Assert.assertEquals(2, smses.size());
        Assert.assertEquals("Bulk1", smses.get(0).getMessage());
        Assert.assertEquals(SmsType.SENT, smses.get(1).getType());
    }
}