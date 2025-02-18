//
//
//	decode.rs
//
//

// parses a file/fifo colines of 512 16-bit float
// those 512 floats then need to be un-(scrambled/rotated?)
// the un-scrambled floats then need to be thresholded into bits
// once they're thresholded, xor them with sha512(callsign)

// thresholding might be a challenge s we dont know what the average
// energy level we'll receive is, and a strong tone could knock that awry


#![feature(f16)]

use std::fs::File;
use std::io::{self, BufReader, Read};


fn sort_f16_arr(array: [f16;512] ) -> [f16; 512] {
  let mut array_s = array;
  array_s.sort_by(|a,b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
  array_s
}

fn avg_pow(data: [f16; 512]) -> f16 {
  let median_output_pow = (sort_f16_arr(data.clone())[31]+sort_f16_arr(data.clone())[32])/2.0;
  median_output_pow
}

fn f16_thresh(data: [f16; 512]) -> [bool; 512] {
  let output = data.map(|z| z<=avg_pow(data));
  output
}

fn bools_to_u8(arr: &[bool; 512]) -> [u8; 64] {
    let mut result = [0u8; 64]; // Resulting array of 64 u8s
    for (i, chunk) in arr.chunks(8).enumerate() {
        let mut byte = 0u8;
        for (j, &bit) in chunk.iter().enumerate() {
            if bit {
                byte |= 1 << j; // Set the bit at position j if the bool is true
            }
        }
        result[i] = byte;
    }
    result
}
fn bytes_to_f16(arr: &[u8; 1024]) -> [f16; 512] {
  let mut result = [0f16; 512]; // Initialize array of 512 f16 values

    for i in 0..512 {
        // Combine two u8s into one f16 value (example logic)
        let high_byte = arr[2 * i];
        let low_byte = arr[2 * i + 1];

        // Combine the two bytes into a 16-bit value (u16)
        let combined = [high_byte, low_byte];

        // Convert the combined 16-bit value into an f16 using from_ne_bytes
        result[i] = f16::from_ne_bytes(combined);

    }

    result
}


fn read_file_in_f16_chunks(file_path: &str) -> io::Result<()> {
    let file = File::open(file_path)?;
    let mut reader = BufReader::new(file);
    let mut u8buffer = [0u8; 1024]; // Buffer to store 61kBbytes at a time

    loop {
        let bytes_read = reader.read(&mut u8buffer)?;

        if bytes_read == 0 {
            break; // End of file reached
        }

        // Process the chunk (here we just print it as hexadecimal for illustration)
        println!("Read {} bytes: {:?}", bytes_read, &u8buffer[..bytes_read]);
        let output_bytes = process_f16_chunk(&bytes_to_f16(&u8buffer));
        println!("Read {} bytes: {:?}", bytes_read, output_bytes);
    }

    Ok(())
}

fn process_f16_chunk(data: &[f16; 512]) -> [u8; 64]{
  return bools_to_u8(&f16_thresh(*data));
}

fn main(){ 
  let _ = read_file_in_f16_chunks("./input.f16");
}
