package net.nczonline.web.props2js;

import org.junit.*;
import static org.junit.Assert.*;
import java.io.*;
import java.util.Properties;

public class Props2JsTest {

    // Helper to create a temp properties file
    private String createTempPropertiesFile(String content) throws IOException {
        File tempFile = File.createTempFile("test", ".properties");
        try (Writer writer = new OutputStreamWriter(new FileOutputStream(tempFile), "UTF-8")) {
            writer.write(content);
        }
        tempFile.deleteOnExit();
        return tempFile.getAbsolutePath();
    }

    @Test
    public void testJsonStdout() throws Exception {
        String props = "foo=bar\nnum=42\nflag=true";
        String file = createTempPropertiesFile(props);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(baos));

        Props2Js.main(new String[] { file });

        System.setOut(oldOut);
        String output = baos.toString("UTF-8");
        assertTrue(output.contains("\"foo\":\"bar\""));
        assertTrue(output.contains("\"num\":42"));
        assertTrue(output.contains("\"flag\":true"));
    }

    @Test
    public void testJsonOutputFile() throws Exception {
        String props = "foo=bar";
        String file = createTempPropertiesFile(props);
        File outFile = File.createTempFile("props2js_test", ".js");
        outFile.deleteOnExit();

        Props2Js.main(new String[] { "-o", outFile.getAbsolutePath(), file });

        String content = new String(java.nio.file.Files.readAllBytes(outFile.toPath()), "UTF-8");
        assertTrue(content.contains("\"foo\":\"bar\""));
    }

    @Test
    public void testJsOutputTypeWithName() throws Exception {
        String props = "foo=bar\nval=5";
        String file = createTempPropertiesFile(props);
        File outFile = File.createTempFile("props2js_test", ".js");
        outFile.deleteOnExit();

        Props2Js.main(new String[] { "-o", outFile.getAbsolutePath(), "-t", "js", "-n", "resultVar", file });

        String content = new String(java.nio.file.Files.readAllBytes(outFile.toPath()), "UTF-8");
        assertTrue(content.startsWith("var resultVar=") || content.startsWith("resultVar="));
        assertTrue(content.contains("\"foo\":\"bar\""));
    }

    @Test
    public void testJsonpOutputTypeWithName() throws Exception {
        String props = "a=1";
        String file = createTempPropertiesFile(props);
        File outFile = File.createTempFile("props2js_test", ".js");
        outFile.deleteOnExit();

        Props2Js.main(new String[] { "-o", outFile.getAbsolutePath(), "-t", "jsonp", "-n", "cb", file });

        String content = new String(java.nio.file.Files.readAllBytes(outFile.toPath()), "UTF-8");
        assertTrue(content.startsWith("cb("));
        assertTrue(content.endsWith(");"));
        assertTrue(content.contains("\"a\":1"));
    }

    @Test
    public void testHelpOption() {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(baos));
        try {
            Props2Js.main(new String[] { "-h" });
        } catch (SecurityException ignore) {
            // System.exit was called; ignore
        }
        finally {
            System.setOut(oldOut);
        }
        String out = baos.toString();
        assertTrue(out.contains("props2js [options]"));
    }

    @Test
    public void testMissingInputFile() {
        Exception ex = null;
        try {
            Props2Js.main(new String[] { });
        } catch (Exception e) {
            ex = e;
        }
        assertNotNull("Should throw on missing input file", ex);
    }

    @Test
    public void testMissingNameWithJsType() throws Exception {
        String props = "x=1";
        String file = createTempPropertiesFile(props);
        Exception ex = null;
        try {
            Props2Js.main(new String[] { "-t", "js", file });
        } catch (Exception e) {
            ex = e;
        }
        assertNotNull("Should throw on missing --name for js", ex);
    }

    @Test
    public void testMissingNameWithJsonpType() throws Exception {
        String props = "x=1";
        String file = createTempPropertiesFile(props);
        Exception ex = null;
        try {
            Props2Js.main(new String[] { "-t", "jsonp", file });
        } catch (Exception e) {
            ex = e;
        }
        assertNotNull("Should throw on missing --name for jsonp", ex);
    }

    @Test
    public void testVerboseLogs() throws Exception {
        String props = "foo=bar";
        String file = createTempPropertiesFile(props);

        ByteArrayOutputStream errBAOS = new ByteArrayOutputStream();
        PrintStream oldErr = System.err;
        System.setErr(new PrintStream(errBAOS));

        File outFile = File.createTempFile("props2js_test", ".js");
        outFile.deleteOnExit();
        Props2Js.main(new String[] { "-v", "-o", outFile.getAbsolutePath(), file });

        System.setErr(oldErr);
        String logs = errBAOS.toString("UTF-8");
        assertTrue(logs.contains("Output file is"));
    }

    @Test
    public void testDefaultOutputTypeIsJson() throws Exception {
        String props = "y=world";
        String file = createTempPropertiesFile(props);

        ByteArrayOutputStream errBAOS = new ByteArrayOutputStream();
        PrintStream oldErr = System.err;
        System.setErr(new PrintStream(errBAOS));

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(baos));

        Props2Js.main(new String[] {"-v", file });

        System.setErr(oldErr);
        System.setOut(oldOut);
        String logs = errBAOS.toString("UTF-8");
        assertTrue(logs.contains("defaulting to json"));
    }
}