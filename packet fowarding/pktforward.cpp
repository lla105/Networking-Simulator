#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

void DecimalToBinary(int num) {
    if (num >= 1) {
        DecimalToBinary(num / 2);
    }
    std::cout << num % 2;
}

void bubblesort(std::vector<std::vector<std::string>>& list) {
    for (int iter_num = list.size() - 1; iter_num > 0; --iter_num) {
        for (int idx = 0; idx < iter_num; ++idx) {
            if (list[idx][2] < list[idx + 1][2]) {
                std::swap(list[idx], list[idx + 1]);
            }
        }
    }
}

std::string deci_to_binary(const std::string& address) {
    std::string full_address = "";
    std::string temp_address = "";
    for (char i : address) {
        if (i == '.') {
            temp_address = std::bitset<8>(std::stoi(temp_address)).to_string();
            full_address += temp_address + ".";
            temp_address = "";
        } else {
            temp_address += i;
        }
    }
    full_address += std::bitset<8>(std::stoi(temp_address)).to_string();
    return full_address;
}

std::string eight_digit_binary(std::string partaddress) {
    if (partaddress.length() == 35) {
        return partaddress;
    } else {
        int dot_pos = 0;
        int eight_count = 0;
        int rangenum = partaddress.length();
        for (int i = 0; i < rangenum; ++i) {
            if (partaddress[i] == '.') {
                dot_pos = i;
                if (eight_count == 8) {
                    continue;
                } else {
                    std::string zeros(8 - dot_pos, '0');
                    partaddress = partaddress.substr(0, dot_pos + 1) + zeros + partaddress.substr(dot_pos + 1);
                }
            }
        }
        return partaddress;
    }
}

std::string bitwise_AND(const std::string& address1, const std::string& address2) {
    std::string product_address = "";
    std::vector<int> dot1list;
    std::vector<int> dot2list;

    for (int i = 0; i < address1.length(); ++i) {
        if (address1[i] == '.') {
            dot1list.push_back(i);
        }
    }

    for (int i = 0; i < address2.length(); ++i) {
        if (address2[i] == '.') {
            dot2list.push_back(i);
        }
    }

    product_address += std::to_string(std::stoi(address1.substr(0, dot1list[0])) & std::stoi(address2.substr(0, dot2list[0]))) + ".";
    product_address += std::to_string(std::stoi(address1.substr(dot1list[0] + 1, dot1list[1])) & std::stoi(address2.substr(dot2list[0] + 1, dot2list[1]))) + ".";
    product_address += std::to_string(std::stoi(address1.substr(dot1list[1] + 1, dot1list[2])) & std::stoi(address2.substr(dot2list[1] + 1, dot2list[2]))) + ".";
    product_address += std::to_string(std::stoi(address1.substr(dot1list[2] + 1)) & std::stoi(address2.substr(dot2list[2] + 1)));

    return product_address;
}

std::vector<std::string> forward_this(const std::string& input_address, const std::vector<std::vector<std::string>>& whole_table) {
    std::vector<int> match_index; // row number
    std::vector<int> metric_value;

    for (int i = 0; i < whole_table.size(); ++i) {
        if (bitwise_AND(input_address, whole_table[i][2]) == whole_table[i][0]) {
            match_index.push_back(i);
            metric_value.push_back(std::stoi(whole_table[i][3]));
        }
    }

    if (match_index.size() > 1) {
        int smallest_metric_index = match_index[0];
        for (int i = 0; i < metric_value.size() - 1; ++i) {
            if (metric_value[i] < metric_value[i + 1]) {
                continue;
            } else if (metric_value[i] == metric_value[i + 1]) {
                continue;
            } else {
                smallest_metric_index = match_index[i + 1];
            }
        }
        return whole_table[smallest_metric_index];
    } else {
        return whole_table[match_index[0]];
    }
}

void printpretty(const std::vector<std::vector<std::string>>& whole_table) {
    std::cout << "Destination    Gateway        mask           metric  interface\n";
    std::cout << "-------------  -------------  -------------  ------  ---------\n";
    for (const auto& row : whole_table) {
        std::string space(14 - row[0].length(), ' ');
        std::string space2(14 - row[1].length(), ' ');
        std::string space3(19 - row[2].length(), ' ');
        std::string space4(2 - row[3].length(), ' ');

        std::cout << row[0] << space << row[1] << space2 << row[2] << space3 << row[3] << space4 << row[4] << '\n';
    }
}

int main() {
    std::string file_name;
    std::cout << "Input your file name WITHOUT inputting the file type\n (eg: If file name is abcd.txt, just type in abcd): ";
    std::cin >> file_name;
    std::cout << "1????";

    std::ifstream file(file_name + ".txt");
    if (!file.is_open()) {
        std::cerr << "Error opening file\n";
        return 1;
    }
    std::cout << "2????";

    std::vector<std::vector<std::string>> whole_table;
    std::vector<std::string> mask_list;

    int count = 0;
    std::string line;
    while (std::getline(file, line)) {
        if (line == "\n" || line == "\r\n") {
            break;
        } else {
            std::vector<std::string> space_split;
            size_t start = 0, end = 0;
            while ((end = line.find(' ', start)) != std::string::npos) {
                space_split.push_back(line.substr(start, end - start));
                start = end + 1;
            }
            space_split.push_back(line.substr(start));
            whole_table.push_back(space_split);
            mask_list.push_back(space_split[2]);
            ++count;
        }
    }

    bubblesort(whole_table);
    printpretty(whole_table);
    std::cout << "-------------------------------------\n";

    std::string addresss1 = deci_to_binary("255.255.254.0");
    std::string addresss2 = deci_to_binary("202.123.40.0");

    bool Continue = true;
    while (Continue) {
        std::cout << '\n';
        std::string user_input;
        std::cout << "Input packet destination IP address: ";
        std::cin >> user_input;

        std::string fake_input = user_input;
        std::vector<std::string> forward_this_row = forward_this(fake_input, whole_table);

        std::cout << forward_this_row[0] << '\n';
        std::cout << "The destination IP address is " << forward_this_row[0] << '\n';
        std::cout << "The next hop IP address is " << forward_this_row[1] << '\n';
        std::cout << "The interface the packet will leave through is " << forward_this_row[4] << '\n';

        std::string next_round;
        std::cout << "Forward another packet? ";
        std::cin >> next_round;
        if (next_round == "yes") {
            continue;
        } else {
            Continue = false;
            break;
        }
    }

    return 0;
}
