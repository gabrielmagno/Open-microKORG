use nom::{
    IResult, 
    bytes::complete::{tag, take_till, take}, 
    sequence::tuple
};

use crate::{
    synthesizer::Program,
    filetype::FileType,
    filetype::base::Base
};

fn parse_sysex(input: &[u8]) -> IResult<&[u8], (&[u8], &[u8], &[u8], &[u8], &[u8])> {
    tuple((
        tag([0xf0]), 
        tag([0x42, 0x30, 0x58]),
        take(1usize),
        take_till(|b| b == 0xf7),
        tag([0xf7])
    ))(input)
}

pub struct SysEx;

impl FileType for SysEx {
    fn decode(data: &[u8]) -> Program {

        let (remaining, (sysex_header, mk_header, mk_func, data, sysex_footer)) = parse_sysex(&data)
            .expect("Errou!");

        println!("Sysex Header: {:02x?}", sysex_header);
        println!("Sysex Footer: {:02x?}", sysex_footer);
        println!("MK Header: {:02x?}", mk_header);
        println!("MK Func: {:02x?}", mk_func);
        println!("Data: {:02x?}", data);
        println!("Remaining: {:02x?}", remaining);

        return Base::decode(data)
    }
    fn encode(program: Program) -> Vec<u8> {
        return Vec::new();
    }
}