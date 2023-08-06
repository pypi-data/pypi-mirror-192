use pyo3::prelude::*;

use std::net::{TcpStream, Shutdown};
use std::io::{Read, Write};
use std::str;
use ed25519_dalek::Keypair;


mod cryptography;

#[pyfunction]
fn test(a: u8, b:u8) -> PyResult<u8>{
    Ok(a as u8+b as u8)
}


fn recv(stream: &mut TcpStream) -> Vec<u8> {
    let mut data = [0 as u8; 50];
    let mut send_data:Vec<u8> = Vec::new();
    let mut read:u32 = 0;
    let mut size:u32 = 0;
    'main: while match stream.read(&mut data) {
        Ok(_) => {
            for byte in data{
                if data == [0; 50] {
                    continue;
                }
                if read == 0{
                    if byte == 255 {
                        break 'main;
                    }
                }
                else if read < 4{
                    size |= (byte as u32) << 8*(3-read);
                }
                else{
                    send_data.push(byte);
                }
                if read == size+3 && read != 0 {
                    return send_data
                }
                else {
                    read += 1;
                }
            }
            true
        },
        Err(_) => {
            println!("An error occurred, terminating connection with {}", stream.peer_addr().unwrap());
            stream.shutdown(Shutdown::Both).unwrap();
            false
        }
    } {} 
    Vec::new()
}

#[pyclass]
struct Connection {
    ip: String,
    stream: TcpStream,
    keys: Keypair
}

#[pymethods]
impl Connection {
    #[new]
    fn new() -> PyResult<Self> {
        let ip = String::from("127.0.0.1:30002");
        let stream = TcpStream::connect(&ip).unwrap();

        Ok(Self {ip: ip, stream: stream, keys: cryptography::get_keys()})
    }

    fn test(&mut self) -> PyResult<Vec<u8>> {
        self.stream.write(&[255]).unwrap();
        Ok(recv(&mut self.stream))
    }

    fn register(&mut self, user_name:String, public_key:String, profile_picture:String, info:String) {
        let mut bytes:Vec<u8> = Vec::new();

        let mut user_name_bytes:Vec<u8> = user_name.as_bytes().to_vec();
        let mut info_bytes:Vec<u8> = info.as_bytes().to_vec();
        let mut public_key_bytes:Vec<u8> = public_key.as_bytes().to_vec();
        let mut profile_picture_bytes:Vec<u8> = profile_picture.as_bytes().to_vec();

        let user_name_len = user_name_bytes.len() as u8;
        let info_len = info_bytes.len() as u8;


        let mut to_sign_data = Vec::new();
        to_sign_data.append(&mut user_name_bytes);
        to_sign_data.append(&mut info_bytes);
        to_sign_data.append(&mut public_key_bytes);
        to_sign_data.append(&mut profile_picture_bytes);

        let signature = cryptography::sign(&to_sign_data, &self.keys);

        let mut size: u32 = 3;
    
        size += to_sign_data.len() as u32;
        size += signature.len() as u32;

        bytes.append(&mut size.to_be_bytes().to_vec());
        bytes.push(64);

        bytes.push(user_name_len);
        bytes.push(info_len);

        bytes.append(&mut to_sign_data);
        bytes.append(&mut signature.as_bytes().to_vec());

        println!("{:?}", bytes);

        self.stream.write(&bytes).unwrap();
        println!("{:?}", recv(&mut self.stream));
    }

    fn get_ip(&self) -> PyResult<&str> {
        Ok(&self.ip)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn doxa_api(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(test, m)?)?;
    m.add_function(wrap_pyfunction!(cryptography::gen_keys, m)?)?;
    m.add_function(wrap_pyfunction!(cryptography::get_pub_key, m)?)?;

    m.add_class::<Connection>()?;
    Ok(())
}