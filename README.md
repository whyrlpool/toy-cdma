
this is a toy CDMA implementation. It's missing a bunch of features at the minute.

The idea was to effectively create a low spectral power density wideband (for HF at least)
CDMA modulator and demodulator, for sending serial data over the air.

The rough idea is as follows
  1. input serial data
  2. xor(sha512(callsign), input)
  3. xor(sha512(block_counter, input)
  4. data_to_bmp(512*block_count, input)
  5. spectrum_paint(28.915MHz, 256kHz, input_bmp)

decoding is similar
  1. take FFT(128.915MHz, 256kHz)
  2. discard phase data (for now, future implementation should use a less ridiculous modulation method)
  3. apply thresholding to raw float output (bool output = ( pixel_value <= median))
  4. turn those bools back into bytes
  5. xor(block_counter, input)
  6. xor(sha512(transmitter_callsign), input)
  7. output serial terminal

steps missing:
  1. serial data interleaving
  2. bit scrambling based off block_counter, so e.g. input_byte[13] isnt always at X kHz
  3. a better thresholding method
  4. time and frequency synch
  5. ARQs, etc. These are left to protocols that go over the top.
  6. LBT, just spectrum paint the data when the band is free by hand for now
  7. a more sane modulation method than spectrum painting, I just wanted very flat PAPR and I thought xor(sha512(callsign),data) and spectrum paint the bits would be a funny start
  8. rest of the fucking owl

There's the decode directory with an example in rust (bad) and python (worse). Maybe one of these will work with the right amount of glue
There's the encode directory with an example in python, which creates a monochrome bitmap to spectrum paint with gr-paint.
take a look in here for an example grc to spectrum paint. Just throw in the bmp and have at it https://github.com/drmpeg/gr-paint/tree/master/apps
