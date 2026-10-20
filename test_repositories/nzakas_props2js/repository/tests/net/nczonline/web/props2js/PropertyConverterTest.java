package net.nczonline.web.props2js;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Properties;

public class PropertyConverterTest {

    @Test
    public void testConvertToJson_withString() {
        Properties p = new Properties();
        p.setProperty("name", "value");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"name\":\"value\""));
    }

    @Test
    public void testConvertToJson_withInt() {
        Properties p = new Properties();
        p.setProperty("intValue", "123");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"intValue\":123"));
    }

    @Test
    public void testConvertToJson_withFloat() {
        Properties p = new Properties();
        p.setProperty("floatValue", "12.34");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"floatValue\":12.34"));
    }

    @Test
    public void testConvertToJson_withBooleanTrue() {
        Properties p = new Properties();
        p.setProperty("flag", "true");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"flag\":true"));
    }

    @Test
    public void testConvertToJson_withBooleanFalse() {
        Properties p = new Properties();
        p.setProperty("flag", "false");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"flag\":false"));
    }

    @Test
    public void testConvertToJsonP() {
        Properties p = new Properties();
        p.setProperty("a", "1");
        String out = PropertyConverter.convertToJsonP(p, "cb");
        assertTrue(out.startsWith("cb("));
        assertTrue(out.endsWith(");"));
    }

    @Test
    public void testConvertToJavaScript_var() {
        Properties p = new Properties();
        p.setProperty("foo", "bar");
        String js = PropertyConverter.convertToJavaScript(p, "testVar");
        assertTrue(js.startsWith("var testVar="));
        assertTrue(js.endsWith(";"));
    }

    @Test
    public void testConvertToJavaScript_assignment() {
        Properties p = new Properties();
        p.setProperty("foo", "bar");
        String js = PropertyConverter.convertToJavaScript(p, "object.property");
        assertFalse(js.startsWith("var "));
        assertTrue(js.startsWith("object.property="));
        assertTrue(js.endsWith(";"));
    }

    @Test
    public void testConvertToJson_withMixedTypes() {
        Properties p = new Properties();
        p.setProperty("string", "text");
        p.setProperty("int", "42");
        p.setProperty("float", "2.718");
        p.setProperty("trueBool", "true");
        p.setProperty("falseBool", "false");
        String json = PropertyConverter.convertToJson(p);
        assertTrue(json.contains("\"string\":\"text\""));
        assertTrue(json.contains("\"int\":42"));
        assertTrue(json.contains("\"float\":2.718"));
        assertTrue(json.contains("\"trueBool\":true"));
        assertTrue(json.contains("\"falseBool\":false"));
    }

    @Test
    public void testConvertToJson_handlesEmptyProperties() {
        Properties p = new Properties();
        String json = PropertyConverter.convertToJson(p);
        assertEquals("{}", json);
    }
}