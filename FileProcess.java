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
                //TODO stage1-Notes_1-删除空行和字符小于1的行。
                /*if (line.trim().length() > 1) {
                    list.add(line);
                    bufferedWriter.write(line + "\t\n");
                    bufferedWriter.flush();
                }*/
                //TODO stage2-Notes_2-删除所有行里面带有数字的,
                //保留包含大小写字符的
                // 并把行后面的换行符空格等空白字符给去掉
                /*if (!line.matches(".*\\d.*") && line.matches(".*[a-zA-Z].*")) {
                    list.add(line);
                    bufferedWriter.write(line.trim() + "\n");
                    bufferedWriter.flush();
                }*/
                //System.out.println(list.size());
                //TODO stage3-对所有行排序并按照倒序排列  <entity> <num>
                //全大写，用于去重
                line = line.toUpperCase();
                //去除网址数据
                if (line.matches(".*WWW\\..*")) {
                    continue;
                }
                //去除结尾冒号
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
