import { NearBindgen, near, call, view } from "near-sdk-js";
@NearBindgen({})
class Hello { greeting = "hi";
  @view({}) get_greeting() { return this.greeting; }
  @call({}) set_greeting({ greeting }) { near.log(`set ${greeting}`); this.greeting = greeting; } }
