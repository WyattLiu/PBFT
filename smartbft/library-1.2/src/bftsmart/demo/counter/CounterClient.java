/**
Copyright (c) 2007-2013 Alysson Bessani, Eduardo Alchieri, Paulo Sousa, and the authors indicated in the @author tags

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package bftsmart.demo.counter;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

import bftsmart.tom.ServiceProxy;
import java.util.Set;
import java.io.*;
import java.net.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;


/**
 * Example client that updates a BFT replicated service (a counter).
 * 
 * @author alysson
 */
public class CounterClient {

    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            System.out.println("Usage: java ... CounterClient <process id> <increment> [<number of operations>]");
            System.out.println("       if <increment> equals 0 the request will be read-only");
            System.out.println("       default <number of operations> equals 1000");
            System.exit(-1);
        }

        ServiceProxy counterProxy = new ServiceProxy(Integer.parseInt(args[0]));
        String RAC_addr = args[1];
        String[] RACs = RAC_addr.split(":");
        String RAC_ip = RACs[0];
        String RAC_port = RACs[1];
	System.out.println("RAC: " + RAC_ip + " port: " + RAC_port);

        try {

            	int inc = 1;
	   	int i = 0;
	    	try (ServerSocket serverSocket = new ServerSocket(3002)) {
		    while(true) {
			ByteArrayOutputStream out = new ByteArrayOutputStream(4);
			new DataOutputStream(out).writeInt(inc);

			System.out.print("Invocation " + i);
			byte[] reply = (inc == 0)?
				counterProxy.invokeUnordered(out.toByteArray()):
				counterProxy.invokeOrdered(out.toByteArray()); //magic happens here
			
			if(reply != null) {
			    	int newValue = new DataInputStream(new ByteArrayInputStream(reply)).readInt();
			    	System.out.println(", returned value: " + newValue);
				// BFT done here
				try(
                                        Socket clientSocket = serverSocket.accept();
                                        //PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
                                        InputStream ins = new BufferedInputStream(clientSocket.getInputStream());
                                        OutputStream outs = new BufferedOutputStream(clientSocket.getOutputStream(), 100);
                                ) {
					String line;
                                        byte[] array = new byte[100];
                                        int size = ins.read(array,0,100);
					String key = new String(array).trim();
					byte[] arrayrac = new byte[100];
                                        String ans = "";
                                        if(key != "") {
						try (
                                                        Socket echoSocket = new Socket(RAC_ip, Integer.parseInt(RAC_port));
                                                        OutputStream outcl = new BufferedOutputStream(echoSocket.getOutputStream(), 100);
                                                        InputStream incl = new BufferedInputStream(echoSocket.getInputStream());
                                                ) {
                                                        // System.out.print("Forwarding to RAC: " + key + "\n");
                                                        outcl.write(array,0,size);
                                                        // System.out.println("Flush");
                                                        outcl.flush();
                                                        // System.out.print("Forwarded to RAC\n");
                                                        size = incl.read(arrayrac,0,100);
                                                        ans = new String(arrayrac).trim();
                                                        // System.out.println("RAC replied byte: " + size);
                                                        echoSocket.close();
                                                } catch (UnknownHostException e) {
                                                    System.err.println("Don't know about host " + RAC_ip);
                                                    System.exit(1);
                                                } catch (IOException e) {
                                                    System.err.println("Couldn't get I/O for the connection to " +
                                                        RAC_ip);
                                                    System.exit(1);
                                                }
                                                // System.out.println("Byte length: " + ans.getBytes().length);
                                                outs.write(ans.getBytes(), 0, ans.getBytes().length);
						
					} else {
                                                clientSocket.close();
                                        } 	
				} catch (IOException ex) {
                                        // System.out.println("Server exception: " + ex.getMessage());
                                        ex.printStackTrace();
                                }

			} else {
			    System.out.println(", ERROR! Exiting.");
			    break;
			}
			i++;
		    }
		} catch (IOException ex) {
                        // System.out.println("Server exception: " + ex.getMessage());
                        ex.printStackTrace();
                } 
        } catch(NumberFormatException e){
            counterProxy.close();
        }
    }
}
