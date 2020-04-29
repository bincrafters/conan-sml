// $CXX -std=c++14 hello_world.cpp
#include <boost/sml.hpp>
#include <cassert>

namespace sml = boost::sml;

namespace {
struct release {};
struct ack {};
struct fin {};
struct timeout {};

const auto is_ack_valid = [](const ack&) { return true; };
const auto is_fin_valid = [](const fin&) { return true; };

const auto send_fin = [] {};
const auto send_ack = [] {};

class established;
class fin_wait_1;
class fin_wait_2;
class timed_wait;

struct hello_world {
  auto operator()() const {
    using namespace sml;
    return make_transition_table(
      *state<established> + event<release> / send_fin = state<fin_wait_1>,
       state<fin_wait_1> + event<ack> [ is_ack_valid ] = state<fin_wait_2>,
       state<fin_wait_2> + event<fin> [ is_fin_valid ] / send_ack = state<timed_wait>,
       state<timed_wait> + event<timeout> / send_ack = X
    );
  }
};
}

int main() {
  using namespace sml;

  sm<hello_world> sm;
  assert(sm.is(state<established>));

  sm.process_event(release{});
  assert(sm.is(state<fin_wait_1>));

  sm.process_event(ack{});
  assert(sm.is(state<fin_wait_2>));

  sm.process_event(fin{});
  assert(sm.is(state<timed_wait>));

  sm.process_event(timeout{});
  assert(sm.is(X));  // released
}
