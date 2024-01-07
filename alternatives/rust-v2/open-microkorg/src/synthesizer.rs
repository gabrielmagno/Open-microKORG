use std::fmt;

pub struct Program {
    pub data: Vec<u8>
}

pub struct ProgramsBank {
    programs: [Program; 128]
}

impl fmt::Display for Program {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:02x?}", self.data)
    }
}