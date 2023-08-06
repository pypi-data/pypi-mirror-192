#ifndef SRC_IFACE_H
#define SRC_IFACE_H

#ifndef HARMONY_COMBINE
#include "value.h"
#include "strbuf.h"
#include "ops.h"
#include "charm.h"
#include "graph.h"
#include "dot.h"
#endif

void iface_write_spec_graph_to_file(struct global *global, const char* filename);
void iface_write_spec_graph_to_json_file(struct global *global, const char* filename);

#endif //SRC_IFACE_H
