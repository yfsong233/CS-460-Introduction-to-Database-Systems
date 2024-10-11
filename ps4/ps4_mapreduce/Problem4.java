/*
 * Problem4.java
 * 
 * CS 460: Problem Set 4
 */

import java.io.IOException;
import java.util.*;

//import javax.naming.Context;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;
//import org.w3c.dom.Text;

public class Problem4 {
    public static class MyMapper
      extends Mapper<Object, Text, Text, IntWritable> 
    {
        public void map(Object key, Text value, Context context)
          throws IOException, InterruptedException 
        {
            String record = value.toString();
            String[] fields = record.split(",");
            // email field is optional
            if (fields.length > 4 && fields[4].contains("@")) {
                String email = fields[4].split(";")[0]; 
                // in case the 4th field is not splitted by comma like awhite1958@yahoo.com;979442.
                String domain = email.substring(email.indexOf("@") + 1);  // e.g. yahoo.com
                context.write(new Text(domain), new IntWritable(1));
            }
        }
      }

    public static class MyReducer
      extends Reducer<Text, IntWritable, Text, LongWritable> 
    {
        public void reduce(Text key, Iterable<IntWritable> values,
			                     Context context)
          throws IOException, InterruptedException 
        {
            long each_domain_count = 0;
            for (IntWritable val : values) {
                each_domain_count += val.get();
            }
            context.write(key, new LongWritable(each_domain_count));

        }
    }

    public static void main(String[] args) throws Exception {
        /* 
         * Configures and runs the MapReduce job for this problem,
         * using the Mapper and Reducer classes that you will 
         * define above.
         * 
         * IMPORTANT: You should NOT actually try to run the program locally.
         * Rather, after eliminating syntax errors, you should 
         * run your program using the Gradescope page we have
         * provided. See the problem set for more details.
         * 
         * You should NOT change this method!
         */

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "problem 4");

        // Specifies the name of the outer class.
        job.setJarByClass(Problem4.class);

        // Specifies the names of the mapper and reducer classes.
        job.setMapperClass(MyMapper.class);
        job.setReducerClass(MyReducer.class);

        // Sets the types for the keys and values output by the reducer.
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        // Sets the types for the keys and values output by the mapper.
        job.setOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        // Configure the type and location of the data being processed.
        job.setInputFormatClass(TextInputFormat.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));

        // Specify where the results should be stored.
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.waitForCompletion(true);
    }
}

