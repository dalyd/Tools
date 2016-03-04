#include <bsoncxx/builder/stream/document.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>

#include <mongocxx/client.hpp>

int main(int argc, char *argv[]) {
  bsoncxx::builder::stream::document mydoc{};
  mongocxx::instance inst{};

  mydoc << "x"
        << "a";
  mongocxx::options::insert options{};
  for (int i = 0; i < 10000; i++) {
    mongocxx::client conn{};
    auto collection = conn["testdb"]["testCollection"];
    collection.insert_one(mydoc.view(), options);
  }
}
