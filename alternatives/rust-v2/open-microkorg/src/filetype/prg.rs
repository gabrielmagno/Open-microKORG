use crate::{
    synthesizer::Program,
    filetype::FileType
};

pub struct Prg;

impl FileType for Prg {
    fn decode(data: &[u8]) -> Program {
        return Program{data: data.to_owned()};
    }
    fn encode(program: Program) -> Vec<u8> {
        return Vec::new();
    }
}