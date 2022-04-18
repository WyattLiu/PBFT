package bftsmart.demo.map;

import java.io.Console;
import java.util.Set;
import java.io.*;
import java.net.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

public class MapInteractiveClient {
	public static void main(String[] args) {
		if(args.length < 1) {
			// System.out.println("Usage: demo.map.MapInteractiveClient <client id>");
		}
		
		int clientId = Integer.parseInt(args[0]);
		MapClient<String, String> map = new MapClient<>(clientId);
		
		// RAC
		String RAC_addr = args[1];
		String[] RACs = RAC_addr.split(":");
		String RAC_ip = RACs[0];
		String RAC_port = RACs[1];
		// System.out.print("RAC: " + RAC_ip + " port: " + RAC_port + "\n");

		boolean exit = false;
		String key, value, result;
		try (ServerSocket serverSocket = new ServerSocket(3002)) {
			while(!exit) {
				try(
					Socket clientSocket = serverSocket.accept(); 
					//PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
					InputStream in = new BufferedInputStream(clientSocket.getInputStream());
					OutputStream out = new BufferedOutputStream(clientSocket.getOutputStream(), 100);
				) {
					String line;
					byte[] array = new byte[100];
					int size = in.read(array,0,100);
					value = "";
					key = new String(array).trim();
					// System.out.println("cmd: " + key + "size: " + size);
					result = map.put(key, value);
					// done with BFT
					byte[] arrayrac = new byte[100];
					String ans = "";
					if(key != "") {
						// System.out.print("RAC code\n");
						try (
							Socket echoSocket = new Socket(RAC_ip, Integer.parseInt(RAC_port));
							OutputStream outc = new BufferedOutputStream(echoSocket.getOutputStream(), 100);
							InputStream inc = new BufferedInputStream(echoSocket.getInputStream());
						) {
							// System.out.print("Forwarding to RAC: " + key + "\n");
							outc.write(array,0,size);
							// System.out.println("Flush");
							outc.flush();
							// System.out.print("Forwarded to RAC\n");
							size = inc.read(arrayrac,0,100);
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
						out.write(ans.getBytes(), 0, ans.getBytes().length);
					} else {
						clientSocket.close();
					}
					// System.out.print("transaction done\n");
				} catch (IOException ex) {
                        		// System.out.println("Server exception: " + ex.getMessage());
                	        	ex.printStackTrace();
		                }

			}
		} catch (IOException ex) {
            		// System.out.println("Server exception: " + ex.getMessage());
            		ex.printStackTrace();
        	}
	}

}
