/*
 * LSST Data Management System
 * See COPYRIGHT file at the top of the source tree.
 *
 * This product includes software developed by the
 * LSST Project (http://www.lsst.org/).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the LSST License Statement and
 * the GNU General Public License along with this program.  If not,
 * see <https://www.lsstcorp.org/LegalNotices/>.
 */

#ifndef LSST_SPHGEOM_PYTHON_RELATIONSHIP_H_
#define LSST_SPHGEOM_PYTHON_RELATIONSHIP_H_

#include "pybind11/pybind11.h"

#include "../Relationship.h"

namespace pybind11 {
namespace detail {

/// This struct is a partial specialization of type_caster for
/// for lsst::sphgeom::Relationship.
///
/// It maps between std::bitset<3> and Python integers, avoiding the need to
/// wrap the former. This header should be included by all wrappers for
/// functions that consume or return Relationship instances.
template <>
struct type_caster<lsst::sphgeom::Relationship> {
public:
    // Declare a local variable `value` of type lsst::sphgeom::Relationship,
    // and describe the Relationship type as an "int" in pybind11-generated
    // docstrings.
    PYBIND11_TYPE_CASTER(lsst::sphgeom::Relationship, _("int"));

    // Convert a Python object to an lsst::sphgeom::Relationship.
    bool load(handle src, bool) {
        value = lsst::sphgeom::Relationship(src.cast<unsigned long long>());
        return true;
    }

    // Convert an lsst::sphgeom::Relationship to a Python integer.
    static handle cast(lsst::sphgeom::Relationship src, return_value_policy,
                       handle) {
        return PyLong_FromUnsignedLong(src.to_ulong());
    }
};

}  // detail
}  // pybind11

#endif  // LSST_SPHGEOM_PYTHON_RELATIONSHIP_H_
