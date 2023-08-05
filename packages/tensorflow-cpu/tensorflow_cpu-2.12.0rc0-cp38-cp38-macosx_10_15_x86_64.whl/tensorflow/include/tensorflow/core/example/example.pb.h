// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/example/example.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fexample_2fexample_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fexample_2fexample_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "tensorflow/core/example/feature.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fexample_2fexample_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fexample_2fexample_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fexample_2fexample_2eproto;
namespace tensorflow {
class Example;
struct ExampleDefaultTypeInternal;
extern ExampleDefaultTypeInternal _Example_default_instance_;
class SequenceExample;
struct SequenceExampleDefaultTypeInternal;
extern SequenceExampleDefaultTypeInternal _SequenceExample_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::Example* Arena::CreateMaybeMessage<::tensorflow::Example>(Arena*);
template<> ::tensorflow::SequenceExample* Arena::CreateMaybeMessage<::tensorflow::SequenceExample>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class Example final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.Example) */ {
 public:
  inline Example() : Example(nullptr) {}
  ~Example() override;
  explicit PROTOBUF_CONSTEXPR Example(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  Example(const Example& from);
  Example(Example&& from) noexcept
    : Example() {
    *this = ::std::move(from);
  }

  inline Example& operator=(const Example& from) {
    CopyFrom(from);
    return *this;
  }
  inline Example& operator=(Example&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const Example& default_instance() {
    return *internal_default_instance();
  }
  static inline const Example* internal_default_instance() {
    return reinterpret_cast<const Example*>(
               &_Example_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(Example& a, Example& b) {
    a.Swap(&b);
  }
  inline void Swap(Example* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(Example* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  Example* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<Example>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const Example& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const Example& from) {
    Example::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(Example* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.Example";
  }
  protected:
  explicit Example(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kFeaturesFieldNumber = 1,
  };
  // .tensorflow.Features features = 1;
  bool has_features() const;
  private:
  bool _internal_has_features() const;
  public:
  void clear_features();
  const ::tensorflow::Features& features() const;
  PROTOBUF_NODISCARD ::tensorflow::Features* release_features();
  ::tensorflow::Features* mutable_features();
  void set_allocated_features(::tensorflow::Features* features);
  private:
  const ::tensorflow::Features& _internal_features() const;
  ::tensorflow::Features* _internal_mutable_features();
  public:
  void unsafe_arena_set_allocated_features(
      ::tensorflow::Features* features);
  ::tensorflow::Features* unsafe_arena_release_features();

  // @@protoc_insertion_point(class_scope:tensorflow.Example)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::tensorflow::Features* features_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fexample_2fexample_2eproto;
};
// -------------------------------------------------------------------

class SequenceExample final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.SequenceExample) */ {
 public:
  inline SequenceExample() : SequenceExample(nullptr) {}
  ~SequenceExample() override;
  explicit PROTOBUF_CONSTEXPR SequenceExample(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  SequenceExample(const SequenceExample& from);
  SequenceExample(SequenceExample&& from) noexcept
    : SequenceExample() {
    *this = ::std::move(from);
  }

  inline SequenceExample& operator=(const SequenceExample& from) {
    CopyFrom(from);
    return *this;
  }
  inline SequenceExample& operator=(SequenceExample&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const SequenceExample& default_instance() {
    return *internal_default_instance();
  }
  static inline const SequenceExample* internal_default_instance() {
    return reinterpret_cast<const SequenceExample*>(
               &_SequenceExample_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(SequenceExample& a, SequenceExample& b) {
    a.Swap(&b);
  }
  inline void Swap(SequenceExample* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(SequenceExample* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  SequenceExample* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<SequenceExample>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const SequenceExample& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const SequenceExample& from) {
    SequenceExample::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(SequenceExample* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.SequenceExample";
  }
  protected:
  explicit SequenceExample(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kContextFieldNumber = 1,
    kFeatureListsFieldNumber = 2,
  };
  // .tensorflow.Features context = 1;
  bool has_context() const;
  private:
  bool _internal_has_context() const;
  public:
  void clear_context();
  const ::tensorflow::Features& context() const;
  PROTOBUF_NODISCARD ::tensorflow::Features* release_context();
  ::tensorflow::Features* mutable_context();
  void set_allocated_context(::tensorflow::Features* context);
  private:
  const ::tensorflow::Features& _internal_context() const;
  ::tensorflow::Features* _internal_mutable_context();
  public:
  void unsafe_arena_set_allocated_context(
      ::tensorflow::Features* context);
  ::tensorflow::Features* unsafe_arena_release_context();

  // .tensorflow.FeatureLists feature_lists = 2;
  bool has_feature_lists() const;
  private:
  bool _internal_has_feature_lists() const;
  public:
  void clear_feature_lists();
  const ::tensorflow::FeatureLists& feature_lists() const;
  PROTOBUF_NODISCARD ::tensorflow::FeatureLists* release_feature_lists();
  ::tensorflow::FeatureLists* mutable_feature_lists();
  void set_allocated_feature_lists(::tensorflow::FeatureLists* feature_lists);
  private:
  const ::tensorflow::FeatureLists& _internal_feature_lists() const;
  ::tensorflow::FeatureLists* _internal_mutable_feature_lists();
  public:
  void unsafe_arena_set_allocated_feature_lists(
      ::tensorflow::FeatureLists* feature_lists);
  ::tensorflow::FeatureLists* unsafe_arena_release_feature_lists();

  // @@protoc_insertion_point(class_scope:tensorflow.SequenceExample)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::tensorflow::Features* context_;
    ::tensorflow::FeatureLists* feature_lists_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fexample_2fexample_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// Example

// .tensorflow.Features features = 1;
inline bool Example::_internal_has_features() const {
  return this != internal_default_instance() && _impl_.features_ != nullptr;
}
inline bool Example::has_features() const {
  return _internal_has_features();
}
inline const ::tensorflow::Features& Example::_internal_features() const {
  const ::tensorflow::Features* p = _impl_.features_;
  return p != nullptr ? *p : reinterpret_cast<const ::tensorflow::Features&>(
      ::tensorflow::_Features_default_instance_);
}
inline const ::tensorflow::Features& Example::features() const {
  // @@protoc_insertion_point(field_get:tensorflow.Example.features)
  return _internal_features();
}
inline void Example::unsafe_arena_set_allocated_features(
    ::tensorflow::Features* features) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.features_);
  }
  _impl_.features_ = features;
  if (features) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.Example.features)
}
inline ::tensorflow::Features* Example::release_features() {
  
  ::tensorflow::Features* temp = _impl_.features_;
  _impl_.features_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::tensorflow::Features* Example::unsafe_arena_release_features() {
  // @@protoc_insertion_point(field_release:tensorflow.Example.features)
  
  ::tensorflow::Features* temp = _impl_.features_;
  _impl_.features_ = nullptr;
  return temp;
}
inline ::tensorflow::Features* Example::_internal_mutable_features() {
  
  if (_impl_.features_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::Features>(GetArenaForAllocation());
    _impl_.features_ = p;
  }
  return _impl_.features_;
}
inline ::tensorflow::Features* Example::mutable_features() {
  ::tensorflow::Features* _msg = _internal_mutable_features();
  // @@protoc_insertion_point(field_mutable:tensorflow.Example.features)
  return _msg;
}
inline void Example::set_allocated_features(::tensorflow::Features* features) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.features_);
  }
  if (features) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(features));
    if (message_arena != submessage_arena) {
      features = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, features, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.features_ = features;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.Example.features)
}

// -------------------------------------------------------------------

// SequenceExample

// .tensorflow.Features context = 1;
inline bool SequenceExample::_internal_has_context() const {
  return this != internal_default_instance() && _impl_.context_ != nullptr;
}
inline bool SequenceExample::has_context() const {
  return _internal_has_context();
}
inline const ::tensorflow::Features& SequenceExample::_internal_context() const {
  const ::tensorflow::Features* p = _impl_.context_;
  return p != nullptr ? *p : reinterpret_cast<const ::tensorflow::Features&>(
      ::tensorflow::_Features_default_instance_);
}
inline const ::tensorflow::Features& SequenceExample::context() const {
  // @@protoc_insertion_point(field_get:tensorflow.SequenceExample.context)
  return _internal_context();
}
inline void SequenceExample::unsafe_arena_set_allocated_context(
    ::tensorflow::Features* context) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.context_);
  }
  _impl_.context_ = context;
  if (context) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.SequenceExample.context)
}
inline ::tensorflow::Features* SequenceExample::release_context() {
  
  ::tensorflow::Features* temp = _impl_.context_;
  _impl_.context_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::tensorflow::Features* SequenceExample::unsafe_arena_release_context() {
  // @@protoc_insertion_point(field_release:tensorflow.SequenceExample.context)
  
  ::tensorflow::Features* temp = _impl_.context_;
  _impl_.context_ = nullptr;
  return temp;
}
inline ::tensorflow::Features* SequenceExample::_internal_mutable_context() {
  
  if (_impl_.context_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::Features>(GetArenaForAllocation());
    _impl_.context_ = p;
  }
  return _impl_.context_;
}
inline ::tensorflow::Features* SequenceExample::mutable_context() {
  ::tensorflow::Features* _msg = _internal_mutable_context();
  // @@protoc_insertion_point(field_mutable:tensorflow.SequenceExample.context)
  return _msg;
}
inline void SequenceExample::set_allocated_context(::tensorflow::Features* context) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.context_);
  }
  if (context) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(context));
    if (message_arena != submessage_arena) {
      context = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, context, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.context_ = context;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.SequenceExample.context)
}

// .tensorflow.FeatureLists feature_lists = 2;
inline bool SequenceExample::_internal_has_feature_lists() const {
  return this != internal_default_instance() && _impl_.feature_lists_ != nullptr;
}
inline bool SequenceExample::has_feature_lists() const {
  return _internal_has_feature_lists();
}
inline const ::tensorflow::FeatureLists& SequenceExample::_internal_feature_lists() const {
  const ::tensorflow::FeatureLists* p = _impl_.feature_lists_;
  return p != nullptr ? *p : reinterpret_cast<const ::tensorflow::FeatureLists&>(
      ::tensorflow::_FeatureLists_default_instance_);
}
inline const ::tensorflow::FeatureLists& SequenceExample::feature_lists() const {
  // @@protoc_insertion_point(field_get:tensorflow.SequenceExample.feature_lists)
  return _internal_feature_lists();
}
inline void SequenceExample::unsafe_arena_set_allocated_feature_lists(
    ::tensorflow::FeatureLists* feature_lists) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.feature_lists_);
  }
  _impl_.feature_lists_ = feature_lists;
  if (feature_lists) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.SequenceExample.feature_lists)
}
inline ::tensorflow::FeatureLists* SequenceExample::release_feature_lists() {
  
  ::tensorflow::FeatureLists* temp = _impl_.feature_lists_;
  _impl_.feature_lists_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::tensorflow::FeatureLists* SequenceExample::unsafe_arena_release_feature_lists() {
  // @@protoc_insertion_point(field_release:tensorflow.SequenceExample.feature_lists)
  
  ::tensorflow::FeatureLists* temp = _impl_.feature_lists_;
  _impl_.feature_lists_ = nullptr;
  return temp;
}
inline ::tensorflow::FeatureLists* SequenceExample::_internal_mutable_feature_lists() {
  
  if (_impl_.feature_lists_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::FeatureLists>(GetArenaForAllocation());
    _impl_.feature_lists_ = p;
  }
  return _impl_.feature_lists_;
}
inline ::tensorflow::FeatureLists* SequenceExample::mutable_feature_lists() {
  ::tensorflow::FeatureLists* _msg = _internal_mutable_feature_lists();
  // @@protoc_insertion_point(field_mutable:tensorflow.SequenceExample.feature_lists)
  return _msg;
}
inline void SequenceExample::set_allocated_feature_lists(::tensorflow::FeatureLists* feature_lists) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.feature_lists_);
  }
  if (feature_lists) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(feature_lists));
    if (message_arena != submessage_arena) {
      feature_lists = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, feature_lists, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.feature_lists_ = feature_lists;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.SequenceExample.feature_lists)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fexample_2fexample_2eproto
