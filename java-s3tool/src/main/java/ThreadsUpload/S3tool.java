package ThreadsUpload;
import com.amazonaws.services.s3.transfer.TransferManager;
import com.amazonaws.services.s3.transfer.TransferManagerBuilder;
import com.amazonaws.services.s3.transfer.MultipleFileUpload;
import com.amazonaws.services.s3.transfer.Download;
import com.amazonaws.services.s3.transfer.MultipleFileDownload;
import com.amazonaws.services.s3.transfer.MultipleFileUpload;
import com.amazonaws.services.s3.transfer.TransferManager;
import com.amazonaws.services.s3.transfer.TransferManagerBuilder;
import com.amazonaws.services.s3.transfer.TransferManagerConfiguration;
import com.amazonaws.services.s3.transfer.Upload;
import com.amazonaws.services.s3.transfer.Download;
import com.amazonaws.services.s3.transfer.TransferManager;
import com.amazonaws.services.s3.transfer.TransferManager;
import com.amazonaws.services.s3.transfer.TransferManagerBuilder;
import com.amazonaws.services.s3.transfer.*;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;
import java.net.URLEncoder;
import java.nio.file.Paths;
import java.util.concurrent.Executors;

import com.amazonaws.AmazonClientException;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.*;

/**
 * 
 *  Class Name: BigFileTest
 *  Function: 
 *  使用高级接口分段上传下载大文件进行测试, 在参数中指定测试文件 对应的bucket, 生成的路径，大小，上传线程数，分片大小，程序会按照这些参数生成文件并进行上传，下载操作，输出测试时刻
 *  Use threads to upload large size files， supply the name of an S3 bucket , a file path to generate , the size of test file and the thread number \n" +
	 the test progam will generate a Big file of the size and use threads  to upload to it
	 
	
 *  As Big Data grows in popularity, it becomes more important to move large data sets to and from Amazon S3.
 *  You can improve the speed of uploads by parallelizing them. 
 *  You can break an individual file into multiple parts and upload those parts in parallel 
 *  by using TransferManager High API
 *  The Multipart upload API enables you to upload large objects in parts. 
 *  You can use this API to upload new large objects 
 *  
 * 
 *  @author chen  DateTime 2018年1月30日 上午10:24
 *  @version 1.0
 */
public class S3tool {



	static final String ACCESS_KEY = "8AXZT7OEX9Y0DQPPVIC1";
	static final String SECRET_KEY = "8XCzirCdv89MxOhP25xZqia6FyY3MucighAIg83Q";
	static final String endpoint = "http://11.11.21.222"; 

	static final long multipartUploadThreshold = 5*1024*1024;
	
	

	public static void downLoadFolder(AmazonS3 client, String keyName , long partSize, String bucketName, int threadnum, String dirname) throws FileNotFoundException
	{
	
		   TransferManager tm = TransferManagerBuilder.standard()
	    	        .withExecutorFactory(() -> Executors.newFixedThreadPool(threadnum))
	    	        .withMinimumUploadPartSize(partSize)
	    	        .withMultipartUploadThreshold( (long) multipartUploadThreshold)
	    	        .withS3Client(client)
	    	        .build();
	        //PART_SIZE was set to 5M.  if object.size < 10M , upload object as a whole , else  The object is divided into 5M pieces 	    				
		   File dir = new File(dirname);
		  
		    try {
		    	 MultipleFileDownload download = tm.downloadDirectory(bucketName, keyName, dir);
		    	 XferMgrProgress.showTransferProgress(download);
		         XferMgrProgress.waitForCompletion(download);

		    }catch (AmazonServiceException e) {
		        System.err.println(e.getErrorMessage());
		        System.exit(1);
		    }
	        finally
	        {
	        	 if(tm != null) {
	                 tm.shutdownNow();
	        	 }
	        }
   }
	
	public static void upLoadFolder(AmazonS3 client, String Dir ,long partSize, String bucketName, int threadnum, String prefix) throws FileNotFoundException
	{
	
		   TransferManager tm = TransferManagerBuilder.standard()
	    	        .withExecutorFactory(() -> Executors.newFixedThreadPool(threadnum))
	    	        .withMinimumUploadPartSize(partSize)
	    	        .withMultipartUploadThreshold( (long) multipartUploadThreshold)
	    	        .withS3Client(client)
	    	        .build();
	        //PART_SIZE was set to 5M.  if object.size < 10M , upload object as a whole , else  The object is divided into 5M pieces 	    
				
		   File dir = new File(Dir);

		   try {
			   MultipleFileUpload upload = tm.uploadDirectory(bucketName,prefix,dir, true);
			   XferMgrProgress.showTransferProgress(upload);
			   XferMgrProgress.waitForCompletion(upload);
		     }catch (AmazonServiceException e) {
			    System.err.println(e.getErrorMessage());
			    System.exit(1);
			}	
	        finally
	        {
	        	 if(tm != null) {
	                 tm.shutdownNow();
	        	 }
	        }
	    }
	
	public static void uploadFile(AmazonS3 client, String filename, long partSize, String bucket, int threadnum, String key ) throws FileNotFoundException
	{
		
		 //Configure about the TransferManger to control your upload.
    	  //When we create the TransferManager, we give it an execution pool of 15 threads. 
    	 //By default, the TransferManager creates a pool of 10,but you can set this to scale the pool size.
    	 //MultipartUploadThreshold defines the size at which the AWS SDK for Java should start breaking apart the files (in this case, 5 MiB).
    	 ///MinimumUploadPartSize defines the minimum size of each part. It must be at least 5 MiB; otherwise, you will get an error when you try to upload it.
		 TransferManager tm = TransferManagerBuilder.standard()
	    	        .withExecutorFactory(() -> Executors.newFixedThreadPool(threadnum))
	    	        .withMinimumUploadPartSize(partSize)
	    	        .withMultipartUploadThreshold( (long) multipartUploadThreshold)
	    	        .withS3Client(client)
	    	        .build();
	        //PART_SIZE was set to 5M.  if object.size < 10M , upload object as a whole , else  The object is divided into 5M pieces 
	      
		   try {
			    File file = new File(filename);
		 		InputStream inputStream = new FileInputStream(file);
		 		ObjectMetadata objectMetadata = new ObjectMetadata();
		 		objectMetadata.setContentLength(file.length());

			
		 		PutObjectRequest putObjectrequest = new PutObjectRequest(
	 			   bucket, key, inputStream, objectMetadata);
	        
		 		Upload upload = tm.upload(putObjectrequest.withCannedAcl(CannedAccessControlList.PublicRead));
				XferMgrProgress.showTransferProgress(upload);
				XferMgrProgress.waitForCompletion(upload);
		   }catch (AmazonServiceException e) {
			    System.err.println(e.getErrorMessage());
			    System.exit(1);
			}	
	        finally
	        {
	        	 if(tm != null) {
	                 tm.shutdownNow();
	        	 }
	        }
	    }
	
	public static void downLoadFile(AmazonS3 client, String keyName , long partSize, String bucketName, int threadnum, String Path) throws FileNotFoundException
	{
	
		   TransferManager tm = TransferManagerBuilder.standard()
	    	        .withExecutorFactory(() -> Executors.newFixedThreadPool(threadnum))
	    	        .withMinimumUploadPartSize(partSize)
	    	        .withMultipartUploadThreshold( (long) multipartUploadThreshold)
	    	        .withS3Client(client)
	    	        .build();
	        //PART_SIZE was set to 5M.  if object.size < 10M , upload object as a whole , else  The object is divided into 5M pieces 	    
		  
		   try {
			    File  file =  new File(Path);
		   		Download download = tm.download(bucketName, keyName, file);
		    	
		    	XferMgrProgress.showTransferProgress(download);
		        XferMgrProgress.waitForCompletion(download);
		   		
		   }catch (AmazonServiceException e) {
			    System.err.println(e.getErrorMessage());
			    System.exit(1);
			}	
	        finally
	        {
	        	 if(tm != null) {
	                 tm.shutdownNow();
	        	 }
	        }
	      
	    }
	
	
	public static void main(String[] args) throws IOException {
		
		final String USAGE = "\n" +
	            "To run this example, supply the name of an S3 bucket , a file path to generate , the size of test file "
	            + "and the thread number \n" +
	            " the test progam will generate a Big file of the size and use threads  to upload to it.\n" +
	            "\n" +
	            "Ex: BigFileTest <bucketname><keyname><threadnum><partSize><filepath><pattern> \n";

        if (args.length < 4) {
	       System.out.println(USAGE);
	       System.exit(1);
        }
      
    	String bucket_name = args[0];
	    String file_path = args[1];
	    String threadnum = args[2];
	    String PartSize = args[3];
	    String dirname = args[4];
	    
	    String pattern = args[5];

	    String key = file_path;

    	long partSize = Long.parseLong(PartSize);
//    	create(file, size);
    	
    	RGWClient	client = new RGWClient(ACCESS_KEY, SECRET_KEY, endpoint);
    	AmazonS3 s3 = client.createConnect();
	    
    	Bucket b = null;
    	if (s3.doesBucketExistV2(bucket_name)) {
            System.out.format("Bucket %s  exists.\n", bucket_name);
        } else {
            try {
                 b = s3.createBucket(bucket_name);
            } catch (AmazonS3Exception e) {
                System.err.println(e.getErrorMessage());
            }
        }
   
    	int num =  Integer.parseInt(threadnum);
//    	upload Big file by sharding and using threads

    	 if(pattern.equals("download"))
    	 {
    		   System.out.println("thread download file begin!");
    		
    		   System.out.println("thread download" + key+ "to local path"+dirname);
    		
    		   long startTime1= System.nanoTime();
    		

    		
    		   downLoadFile(s3, key,partSize,bucket_name, num, dirname );
    		
    	       long endTime1 = System.nanoTime(); //获取结束时间  
    	       System.out.println("thread download run time： "+(endTime1-startTime1)/1000/1000/1000+"s");  
    	 }else if(pattern.equals("upload"))
    	{

    		 	System.out.println("thread upload begin!");
    		 	System.out.println("thread upload " + dirname + "to s3 path" + key);
    		 	long startTime2 = System.nanoTime();
    		 	File file = new File(dirname);
    		 	if (file.isFile())
    		 	{
    		 		uploadFile(s3, dirname, partSize, bucket_name, num, key);
    		 	}else {
    		 		upLoadFolder(s3, dirname, partSize, bucket_name, num, key);
    		 	}
    		
    		 	long endTime2=System.nanoTime(); //获取结束时间  
    		 	System.out.println("thread upload run time： "+(endTime2-startTime2)/1000/1000/1000+"s"); 
    	}

        
}
}

