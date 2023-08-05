/* Copyright 2017 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_CORE_LIB_MONITORING_GAUGE_H_
#define TENSORFLOW_CORE_LIB_MONITORING_GAUGE_H_

#include "tensorflow/core/lib/monitoring/collection_registry.h"
#include "tensorflow/core/lib/monitoring/metric_def.h"
#include "tensorflow/tsl/lib/monitoring/gauge.h"
// NOLINTBEGIN(misc-unused-using-decls)
namespace tensorflow {
namespace monitoring {
using tsl::monitoring::Gauge;
using tsl::monitoring::GaugeCell;

}  // namespace monitoring
}  // namespace tensorflow
// NOLINTEND(misc-unused-using-decls)
#endif  // TENSORFLOW_CORE_LIB_MONITORING_GAUGE_H_
