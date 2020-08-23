import java.io.*;
import java.util.*;

public class FileProcess {
    public static void main(String[] args) {
        long start = Calendar.getInstance().getTimeInMillis();
        try {
            String filePath = "D:/test/Notes_2.txt";
            File outfilePath = new File("D:/test/Notes_3.txt");
            FileReader fileReader = new FileReader(filePath);
            BufferedReader bufferedReader = new BufferedReader(fileReader);

            outfilePath.createNewFile();
            FileWriter fileWriter = new FileWriter(outfilePath);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

            String line = "";
            String reg = "";
            List<String> list = new ArrayList<>();
            Map<String, Integer> map = new HashMap<>();
            int count = 1;
            while ((line = bufferedReader.readLine()) != null) {
     
                line = line.toUpperCase();
         
                if (line.matches(".*WWW\\..*")) {
                    continue;
                }
 
                if (line.endsWith(":")) {
                    line = line.substring(0, line.length() - 1);
                }
                if (map.containsKey(line)) {
                    map.put(line, map.get(line) + 1);
                } else {
                    map.put(line, 1);
                }
            }

            Map<String, Integer> sortedMap = sortUtils.sortMapByValues(map);
            for (Map.Entry<String, Integer> item : sortedMap.entrySet()) {
                bufferedWriter.write(item.getKey() + " " + item.getValue() + "\n");
                bufferedWriter.flush();
            }

            System.out.println(sortedMap.size());

            bufferedReader.close();
            bufferedWriter.close();

            long end = Calendar.getInstance().getTimeInMillis();
            System.out.println(end - start);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
