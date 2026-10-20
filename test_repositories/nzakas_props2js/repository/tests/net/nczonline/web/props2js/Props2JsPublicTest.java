package net.nczonline.web.props2js;

import org.junit.*;
import static org.junit.Assert.*;
import java.io.*;
import java.util.Properties;

public class Props2JsPublicTest {

    // Helper to create a temp properties file
    private String createTempPropertiesFile(String content) throws IOException {
        File tempFile = File.createTempFile("publictest", ".properties");
        try (Writer writer = new OutputStreamWriter(new FileOutputStream(tempFile), "UTF-8")) {
            writer.write(content);
        }
        tempFile.deleteOnExit();
        return tempFile.getAbsolutePath();
    }

    @Test
    public void testJsonStdout_public() throws Exception {
        String props = "hello=world\ncount=128\nenabled=false";
        String file = createTempPropertiesFile(props);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(baos));

        Props2Js.main(new String[] { file });

        System.setOut(oldOut);
        String output = baos.toString("UTF-8");
        assertTrue(output.contains("\"hello\":\"world\""));
        assertTrue(output.contains("\"count\":128"));
        assertTrue(output.contains("\"enabled\":false"));
    }

    @Test
    public void testJsonOutputFile_public() throws Exception {
        String props = "baz=qux";
        String file = createTempPropertiesFile(props);
        File outFile = File.createTempFile("props2js_public", ".js");
        outFile.deleteOnExit();

        Props2Js.main(new String[] { "-o", outFile.getAbsolutePath(), file });

        String content = new String(java.nio.file.Files.readAllBytes(outFile.toPath()), "UTF-8");
        assertTrue(content.contains("\"baz\":\"qux\""));
    }

    @Test
    public void testJsOutputTypeWithName_public() throws Exception {
        String props = "alpha=omega\nnumval=12";
        String file = createTempPropertiesFile(props);
        File outFile = File.createTempFile("props2js_public", ".js");
        outFile.deleteOnExit();

        Props2Js.main(new String[] { "-o", outFile.getAbsolutePath(), "-t", "js", "-n", "newVar", file });

        String content = new String(java.nio.file.Files.readAllBytes(outFile.toPath()), "UTF-8");
        assertTrue(content.startsWith("var newVar=") || content.startsWith("newVar="));
        assertTrue(content.contains("\"alpha\":\"omega\""));
    }

    @Test
    public void testJsonpOutputTypeWithName_public() throws Exception {
        String props = "b=22";
        String file = createTempPropertiesFile(props);
        File outFile = File.createTempFile("props2js_public", ".js");
        outFile.deleteOnExit();

        Props2Js.main(new String[] { "-o", outFile.getAbsolutePath(), "-t", "jsonp", "-n", "fCallback", file });

        String content = new String(java.nio.file.Files.readAllBytes(outFile.toPath()), "UTF-8");
        assertTrue(content.startsWith("fCallback("));
        assertTrue(content.endsWith(");"));
        assertTrue(content.contains("\"b\":22"));
    }

    @Test
    public void testHelpOption_public() {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(baos));
        try {
            Props2Js.main(new String[] { "--help" });
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
    public void testMissingInputFile_public() {
        Exception ex = null;
        try {
            Props2Js.main(new String[] { "--output", "nofile.js" });
        } catch (Exception e) {
            ex = e;
        }
        assertNotNull("Should throw on missing input file", ex);
    }

    @Test
    public void testMissingNameWithJsType_public() throws Exception {
        String props = "some=99";
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
    public void testMissingNameWithJsonpType_public() throws Exception {
        String props = "some=88";
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
    public void testVerboseLogs_public() throws Exception {
        String props = "welcome=here";
        String file = createTempPropertiesFile(props);

        ByteArrayOutputStream errBAOS = new ByteArrayOutputStream();
        PrintStream oldErr = System.err;
        System.setErr(new PrintStream(errBAOS));

        File outFile = File.createTempFile("props2js_public", ".js");
        outFile.deleteOnExit();
        Props2Js.main(new String[] { "-v", "-o", outFile.getAbsolutePath(), file });

        System.setErr(oldErr);
        String logs = errBAOS.toString("UTF-8");
        assertTrue(logs.contains("Output file is"));
    }

    @Test
    public void testDefaultOutputTypeIsJson_public() throws Exception {
        String props = "foo=barz";
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