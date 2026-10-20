package net.nczonline.web.props2js;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Properties;

public class PropertyConverterPublicTest {

    @Test
    public void testConvertToJson_withString_public() {
        Properties p = new Properties();
        p.setProperty("color", "blue");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"color\":\"blue\""));
    }

    @Test
    public void testConvertToJson_withInt_public() {
        Properties p = new Properties();
        p.setProperty("answer", "42");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"answer\":42"));
    }

    @Test
    public void testConvertToJson_withFloat_public() {
        Properties p = new Properties();
        p.setProperty("ratio", "3.14");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"ratio\":3.14"));
    }

    @Test
    public void testConvertToJson_withBooleanTrue_public() {
        Properties p = new Properties();
        p.setProperty("active", "true");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"active\":true"));
    }

    @Test
    public void testConvertToJson_withBooleanFalse_public() {
        Properties p = new Properties();
        p.setProperty("deleted", "false");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"deleted\":false"));
    }

    @Test
    public void testConvertToJsonP_public() {
        Properties p = new Properties();
        p.setProperty("score", "77");
        String out = PropertyConverter.convertToJsonP(p, "pubcb");
        assertTrue(out.startsWith("pubcb("));
        assertTrue(out.endsWith(");"));
    }

    @Test
    public void testConvertToJavaScript_var_public() {
        Properties p = new Properties();
        p.setProperty("animal", "cat");
        String js = PropertyConverter.convertToJavaScript(p, "pubVar");
        assertTrue(js.startsWith("var pubVar="));
        assertTrue(js.endsWith(";"));
    }

    @Test
    public void testConvertToJavaScript_assignment_public() {
        Properties p = new Properties();
        p.setProperty("animal", "dog");
        String js = PropertyConverter.convertToJavaScript(p, "globals.pet");
        assertFalse(js.startsWith("var "));
        assertTrue(js.startsWith("globals.pet="));
        assertTrue(js.endsWith(";"));
    }

    @Test
    public void testConvertToJson_withMixedTypes_public() {
        Properties p = new Properties();
        p.setProperty("note", "hello");
        p.setProperty("age", "30");
        p.setProperty("pi", "3.1416");
        p.setProperty("success", "true");
        p.setProperty("error", "false");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"note\":\"hello\""));
        assertTrue(json.contains("\"age\":30"));
        assertTrue(json.contains("\"pi\":3.1416"));
        assertTrue(json.contains("\"success\":true"));
        assertTrue(json.contains("\"error\":false"));
    }

    @Test
    public void testConvertToJson_handlesEmptyProperties_public() {
        Properties p = new Properties();
        String json = PropertyConverter.convertToJson(p);
        assertEquals("{}", json);
    }
}