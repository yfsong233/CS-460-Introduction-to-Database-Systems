/*
 * Problem5.java
 * 
 * CS 460: Problem Set 4
 */

import java.io.IOException;
import java.util.*;

import javax.naming.Context;

// import javax.naming.Context;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;
// import org.w3c.dom.Text;

public class Problem5 {
    /*** mapper and reducer for the first job in the chain */
    public static class MyMapper1
      extends Mapper<Object, Text, Text, IntWritable> 
    {
        public void map(Object key, Text value, Context context)
          throws IOException, InterruptedException{
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

    public static class MyReducer1
      extends Reducer<Text, IntWritable, Text, LongWritable> 
    {
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
          throws IOException, InterruptedException {
              long each_domain_count = 0;
              for (IntWritable val : values) {
              each_domain_count += val.get();
              }
              context.write(key, new LongWritable(each_domain_count));

        }
    }

    /*** mapper and reducer for the second job in the chain */
    public static class MyMapper2
      extends Mapper<Object, Text, Text, LongWritable> 
    {
        private final static Text argmaxKey = new Text("domain_maxfreq");  // CANNOT CHANGE

        public void map(Object key, Text value, Context context)
          throws IOException, InterruptedException {
              context.write(argmaxKey, value);
        }
    }

    public static class MyReducer2
      extends Reducer<Text, Text, Text, LongWritable> 
    {
        public void reduce(Text key, Iterable<Text> values, Context context)
          throws IOException, InterruptedException {
              int maxCount = 0;
              String maxDomain = null;

              /*
               * kv pair example: 
               * 0            1
               * gmail.com(\t)250
              */
              for (Text val : values) { 
                  String[] kv = val.toString().split("\t");
              if (kv.length < 2) {
                  continue; // invalid length of kv pair
              }

              String domain = kv[0];
              int count = Integer.parseInt(kv[1]);

              if (count > maxCount) {
                  maxCount = count;
                  maxDomain = domain;
              }
        }

        if (maxDomain != null) {
            context.write(new Text(maxDomain), new LongWritable(maxCount));
        }
        }
    }

    public static void main(String[] args) throws Exception {
        /*
         * First job in the chain of two jobs
         */
        Configuration conf = new Configuration();
        Job job1 = Job.getInstance(conf, "problem 5-1");
        job1.setJarByClass(Problem5.class);

        // Specifies the names of the first job's mapper and reducer classes.
        job1.setMapperClass(MyMapper1.class);
        job1.setReducerClass(MyReducer1.class);

        // Sets the types for the keys and values output by the first reducer.
        /* CHANGE THE CLASS NAMES AS NEEDED IN THESE TWO METHOD CALLS */
        job1.setOutputKeyClass(Text.class);
        job1.setOutputValueClass(LongWritable.class);

        // Sets the types for the keys and values output by the first mapper.
        /* CHANGE THE CLASS NAMES AS NEEDED IN THESE TWO METHOD CALLS */
        job1.setOutputKeyClass(Text.class);
        job1.setMapOutputValueClass(IntWritable.class);

        // Configure the type and location of the data processed by job1.
        job1.setInputFormatClass(TextInputFormat.class);
        FileInputFormat.addInputPath(job1, new Path(args[0]));

        // Specify where job1's results should be stored.
        FileOutputFormat.setOutputPath(job1, new Path(args[1]));

        job1.waitForCompletion(true);

        /*
         * Second job the chain of two jobs
         */
        conf = new Configuration();
        Job job2 = Job.getInstance(conf, "problem 5-2");
        job2.setJarByClass(Problem5.class);

        // Specifies the names of the first job's mapper and reducer classes.
        job2.setMapperClass(MyMapper2.class);
        job2.setReducerClass(MyReducer2.class);

        // Sets the types for the keys and values output by the second reducer.
        /* CHANGE THE CLASS NAMES AS NEEDED IN THESE TWO METHOD CALLS */
        job2.setOutputKeyClass(Text.class);
        job2.setOutputValueClass(LongWritable.class);

        // Sets the types for the keys and values output by the first mapper.
        /* CHANGE THE CLASS NAMES AS NEEDED IN THESE TWO METHOD CALLS */
        job2.setOutputKeyClass(Text.class);
        job2.setMapOutputValueClass(Text.class);

        // Configure the type and location of the data processed by job2.
        // Note that its input path is the output path of job1!
        job2.setInputFormatClass(TextInputFormat.class);
        FileInputFormat.addInputPath(job2, new Path(args[1]));
        FileOutputFormat.setOutputPath(job2, new Path(args[2]));

        job2.waitForCompletion(true);
    }
}
