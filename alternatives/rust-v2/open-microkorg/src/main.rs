mod synthesizer;
mod filetype;

use filetype::FileType;

use crate::filetype::sysex::SysEx;

fn main() {
    println!(
        "Program: {}",
        SysEx::read_file("dumps/original-p_a11.syx")
    );
}
