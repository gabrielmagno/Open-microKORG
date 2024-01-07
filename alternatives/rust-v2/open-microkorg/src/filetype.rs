pub mod base;
pub mod prg;
pub mod sysex;

use crate::synthesizer::Program;

pub trait FileType {
    fn decode(data: &[u8]) -> Program;
    fn encode(program: Program) -> Vec<u8>;
    fn read_file(file_name: &str) -> Program {
        let bytes = std::fs::read(file_name)
            .expect(&format!("cannot read file {}", file_name));
        return Self::decode(&bytes);
    }
}
