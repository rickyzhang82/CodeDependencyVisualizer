#include <utility>      // std::pair, std::make_pair
#include <string>       // std::string

class TestType1 {
    public:
        int i;
};

class TestType2 {
    public:
        int i;
};

class TestPair {
    public:
        std::pair<TestType1, TestType2> test_pair;
};

int main () {
  TestPair product;                     // default constructor
 return 0;
}
