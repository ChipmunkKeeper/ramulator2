#include <filesystem>
#include <iostream>
#include <fstream>

#include "frontend/frontend.h"
#include "base/exception.h"

namespace Ramulator {

namespace fs = std::filesystem;

class LoadStoreTrace : public IFrontEnd, public Implementation {
  RAMULATOR_REGISTER_IMPLEMENTATION(IFrontEnd, LoadStoreTrace, "LoadStoreTrace", "Load/Store memory address trace.")

  private:
    struct Trace {
      bool is_write;
      Addr_t addr;
    };
    std::vector<Trace> m_trace;

    size_t m_trace_length = 0;
    size_t m_curr_trace_idx = 0;
    size_t m_trace_count = 0;

    Logger_t m_logger;

  public:
    void init() override {
      std::string trace_path_str = param<std::string>("path").desc("Path to the load store trace file.").required();
      m_clock_ratio = param<uint>("clock_ratio").required();

      m_logger = Logging::create_logger("LoadStoreTrace");
      m_logger->info("Loading trace file {} ...", trace_path_str);
      init_trace(trace_path_str);
      m_logger->info("Loaded {} lines.", m_trace.size());
    };

    void tick() override {
      if (m_curr_trace_idx >= m_trace_length) {
          return;
      }

      const Trace& t = m_trace[m_curr_trace_idx];

      // 尝试发送请求
      // 如果 Controller 缓冲区满了，send 会返回 false
      bool request_sent = m_memory_system->send({
          t.addr, 
          t.is_write ? Request::Type::Write : Request::Type::Read
      });
      
      if (request_sent) {
        // 只有发送成功了，才移动到下一条 Trace
        m_curr_trace_idx++;
        m_trace_count++;
      }
      // 如果发送失败 (false)，直接 return，下一周期 (tick) 再重试同一条指令
      // 这样天然形成了流控，不会堵死控制器
    };

  private:
    void init_trace(const std::string& file_path_str) {
      fs::path trace_path(file_path_str);
      if (!fs::exists(trace_path)) throw ConfigurationError("Trace {} does not exist!", file_path_str);
      std::ifstream trace_file(trace_path);
      if (!trace_file.is_open()) throw ConfigurationError("Trace {} cannot be opened!", file_path_str);

      std::string line;
      while (std::getline(trace_file, line)) {
        std::vector<std::string> tokens;
        tokenize(tokens, line, " ");
        if (tokens.size() != 2) throw ConfigurationError("Trace format invalid!");

        bool is_write = (tokens[0] == "ST");
        Addr_t addr = -1;
        if (tokens[1].compare(0, 2, "0x") == 0 || tokens[1].compare(0, 2, "0X") == 0) {
          addr = std::stoll(tokens[1].substr(2), nullptr, 16);
        } else {
          addr = std::stoll(tokens[1]);
        }
        m_trace.push_back({is_write, addr});
      }
      trace_file.close();
      m_trace_length = m_trace.size();
    };

    bool is_finished() override {
      return m_curr_trace_idx >= m_trace_length; 
    };
};

} // namespace Ramulator