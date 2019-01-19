package cn.itcast.zk;

import org.I0Itec.zkclient.IZkChildListener;
import org.I0Itec.zkclient.ZkClient;
import org.apache.curator.RetryPolicy;
import org.apache.curator.RetrySleeper;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.cache.PathChildrenCache;
import org.apache.curator.framework.recipes.cache.PathChildrenCacheEvent;
import org.apache.curator.framework.recipes.cache.PathChildrenCacheListener;
import org.apache.curator.retry.ExponentialBackoffRetry;

import org.apache.curator.retry.RetryUntilElapsed;
import org.apache.zookeeper.*;

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;


class ExitPolicy implements RetryPolicy {
    ExitPolicy(){}
    public boolean allowRetry(int var1, long var2, RetrySleeper var4) {
        System.exit(1);
        return false;
    }
};


public class TestZKClient {


    public static void sendPost(String url, String param) {
        PrintWriter out = null;
        BufferedReader in = null;
        String result = "";

        int flag;
        do {
            flag = 0;
            try {
                URL realUrl = new URL(url);
                // 打开和URL之间的连接
                URLConnection conn = realUrl.openConnection();
                // 设置通用的请求属性
                conn.setRequestProperty("accept", "*/*");
                conn.setRequestProperty("connection", "Keep-Alive");
                conn.setRequestProperty("user-agent",
                        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)");
                // 发送POST请求必须设置如下两行
                conn.setDoOutput(true);
                conn.setDoInput(true);
                // 获取URLConnection对象对应的输出流
                out = new PrintWriter(conn.getOutputStream());
                // 发送请求参数
                out.print(param);
                // flush输出流的缓冲
                out.flush();
                // 定义BufferedReader输入流来读取URL的响应
                in = new BufferedReader(
                        new InputStreamReader(conn.getInputStream()));
                String line;
                while ((line = in.readLine()) != null) {
                    result += line;
                }
            } catch (Exception e) {
                System.out.println("发送 POST 请求出现异常！"+e);
                flag = 1;
                e.printStackTrace();
            }
            //使用finally块来关闭输出流、输入流
            finally{
                try{
                    if(out!=null){
                        out.close();
                    }
                    if(in!=null){
                        in.close();
                    }
                }
                catch(IOException ex){
                    ex.printStackTrace();
                }
            }
        }while(flag==1);
        System.out.println(result);
        return;
    }


    public  static InetAddress getFirstNonLoopbackAddress(boolean preferIpv4, boolean preferIPv6) throws SocketException {
        Enumeration en = NetworkInterface.getNetworkInterfaces();
        while (en.hasMoreElements()) {
            NetworkInterface i = (NetworkInterface) en.nextElement();
            for (Enumeration en2 = i.getInetAddresses(); en2.hasMoreElements();) {
                InetAddress addr = (InetAddress) en2.nextElement();
                if (!addr.isLoopbackAddress()) {
                    if (addr instanceof Inet4Address) {
                        if (preferIPv6) {
                            continue;
                        }
                        return addr;
                    }
                    if (addr instanceof Inet6Address) {
                        if (preferIpv4) {
                            continue;
                        }
                        return addr;
                    }
                }
            }
        }
        return null;
    }

    public static List<String> cluster_list;
    public static String myid;

    public static void main(String[] args) throws Exception {


//          String clusterPath = "/cluster";
//          String serverPath = "/server";
//          String myid = "me";
//
//          ZkClient zk = new ZkClient("localhost:2181",5000);
//
////          int conn_flag;
////          do {
////              conn_flag = 0;
////              try {
////                  zk = new ZkClient("localhost:2181",5000);
////              } catch(Exception ex) {
////                  conn_flag = 1;
////              };
////          }while(conn_flag==1);
//
//
//          if(!zk.exists(clusterPath)) {
//              zk.createPersistent(clusterPath);
//          }
//
//          zk.createEphemeral(clusterPath + "/" + myid);
//
//          if(!zk.exists(serverPath)) {
//              zk.createEphemeral(serverPath);
//              zk.writeData(serverPath,myid);
//          }
//
//        System.out.println(zk.readData(serverPath));
//
//
//
//
//
//          zk.subscribeChildChanges(clusterPath, new IZkChildListener() {
//              public void handleChildChange(String s, List<String> list) throws Exception {
//                  String id = zk.readData()
//                  if(myid == )
//                  System.out.println(s+" 's child changed, currentChilds:"+list);
//                  new Thread
//              }
//          });
//
//          zk.subscribeChildChanges(serverPath, new IZkChildListener() {
//              public void handleChildChange(String s, List<String> list) throws Exception {
//                  System.out.println(s+" 's child changed, currentChilds:"+list);
//              }
//          });


            final String clusterPath = "/cluster";
            final String serverPath = "/server";
            final String url = "http://localhost:8000";

            cluster_list = new ArrayList<String>();
            myid = getFirstNonLoopbackAddress(true,false).getHostAddress();


            RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000,10);
            final CuratorFramework client = CuratorFrameworkFactory.builder()
                                                        .connectString("localhost:2181")
                                                        .sessionTimeoutMs(5000)
                                                        .retryPolicy(retryPolicy)
                                                        .build();
            client.start();

            if(client.checkExists().forPath(clusterPath)==null) {
                client.create().forPath(clusterPath);
            }

            client.create().withMode(CreateMode.EPHEMERAL).forPath(clusterPath+"/"+myid);

            if(client.checkExists().forPath(serverPath)==null) {
                client.create().withMode(CreateMode.EPHEMERAL).forPath(serverPath);
                client.setData().forPath(serverPath,myid.getBytes());
            }


            PathChildrenCache cluster_cache = new PathChildrenCache(client,clusterPath,true);
            cluster_cache.start();
            cluster_cache.getListenable().addListener(new PathChildrenCacheListener() {
                public void childEvent(CuratorFramework curatorFramework, PathChildrenCacheEvent pathChildrenCacheEvent) throws Exception {
                    cluster_list = client.getChildren().forPath(clusterPath);
                }
            });

            PathChildrenCache server_cache = new PathChildrenCache(client,"/",true);
            server_cache.start();
            server_cache.getListenable().addListener(new PathChildrenCacheListener() {
                public void childEvent(CuratorFramework curatorFramework, PathChildrenCacheEvent pathChildrenCacheEvent) throws Exception {
                    if(client.checkExists().forPath(serverPath)==null) {
                        client.create().withMode(CreateMode.EPHEMERAL).forPath(serverPath);
                        client.setData().forPath(serverPath,myid.getBytes());
                    }
                }
            });


            while(true) {
                if(client.checkExists().forPath(serverPath)!=null) {
                    String current_server_id = new String(client.getData().forPath(serverPath));
                    System.out.println(current_server_id+" "+myid);
                    System.out.println(current_server_id.equals(myid));
                    if(current_server_id.equals(myid)) {
                        List<String> current_cluster_list = cluster_list;
                        String param = "";
                        for(int i=0;i<current_cluster_list.size();i++) {
                            param += " ";
                            param += current_cluster_list.get(i);
                            param += " ";
                        }
                        //sendPost(url,param);
                        try {
                            Socket socket = new Socket("localhost",8001);
                            //获取输出流，向服务器端发送信息
                            OutputStream os=socket.getOutputStream();//字节输出流
                            PrintWriter pw=new PrintWriter(os);//将输出流包装为打印流
                            pw.write(param+" "+current_server_id+" "+myid);
                            pw.flush();
                            socket.shutdownOutput();//关闭输出流
                            //socket.close();
                        } catch (UnknownHostException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }

                    }
                }

                Thread.sleep(1000);
            }

    }
}
