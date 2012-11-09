#include <fstream>
#include "pugixml.hpp"
#include <iostream>
#include <string>
#include <sstream>
#include <utility>

#define DELIMITER "#OppanOCRplusDelimiter#"

int main(int argc, char * argv[]) {
	std::string del=DELIMITER;
	std::ofstream fout(argv[2]);
	pugi::xml_document doc;
	pugi::xml_parse_result result = doc.load_file(argv[1]);
	pugi::xml_node html = doc.child("html");
	pugi::xml_node body = html.child("body");
	pugi::xml_node ps = body.child("div").child("div");

	for (pugi::xml_node p = ps.child("p"); p; p = p.next_sibling("p")) {
		std::string para;
		for (pugi::xml_node sent = p.child("span"); sent; sent = sent.next_sibling("span")) {
			std::string bbox = sent.attribute("title").value();
			bbox=bbox.substr(5);
			std::string tmp;
			bool first=true;
			for (pugi::xml_node word = sent.child("span"); word; word = word.next_sibling("span")) {
				std::string cur = word.child_value();
				if(!first) tmp+=" ";
				tmp+=cur;
				first=false;
			}
			para+=bbox+del+tmp+del;
		}
		fout << para << std::endl;
	}
	return 0;
}
