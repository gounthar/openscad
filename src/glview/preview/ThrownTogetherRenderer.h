#pragma once

#include <memory>
#include <cstddef>
#include <vector>

#include "glview/Renderer.h"
#include "core/CSGNode.h"

#include "glview/VBORenderer.h"

class CSGProducts;
class CSGChainObject;

class TTRVertexState : public VertexState
{
public:
  TTRVertexState(size_t csg_object_index = 0)
    : csg_object_index_(csg_object_index) {}
  TTRVertexState(GLenum draw_mode, GLsizei draw_size, GLenum draw_type,
                 size_t draw_offset, size_t element_offset, GLuint vertices_vbo, GLuint elements_vbo,
                 size_t csg_object_index = 0)
    : VertexState(draw_mode, draw_size, draw_type, draw_offset, element_offset, vertices_vbo, elements_vbo), csg_object_index_(csg_object_index)
  {}

  [[nodiscard]] size_t csgObjectIndex() const { return csg_object_index_; }
  void setCsgObjectIndex(size_t csg_object_index) { csg_object_index_ = csg_object_index; }

private:
  size_t csg_object_index_;
};

class TTRVertexStateFactory : public VertexStateFactory
{
public:
  TTRVertexStateFactory() = default;

  [[nodiscard]] std::shared_ptr<VertexState> createVertexState(GLenum draw_mode, size_t draw_size, GLenum draw_type,
                                                               size_t draw_offset, size_t element_offset,
                                                               GLuint vertices_vbo, GLuint elements_vbo) const override {
    return std::make_shared<TTRVertexState>(draw_mode, draw_size, draw_type, draw_offset, element_offset, vertices_vbo, elements_vbo);
  }
};

class ThrownTogetherRenderer : public VBORenderer
{
public:
  ThrownTogetherRenderer(std::shared_ptr<CSGProducts> root_products,
                         std::shared_ptr<CSGProducts> highlight_products,
                         std::shared_ptr<CSGProducts> background_products);
  ~ThrownTogetherRenderer() override;
  void prepare(bool showfaces, bool showedges, const RendererUtils::ShaderInfo *shaderinfo = nullptr) override;
  void draw(bool showfaces, bool showedges, const RendererUtils::ShaderInfo *shaderinfo = nullptr) const override;

  BoundingBox getBoundingBox() const override;
private:
  void renderCSGProducts(const std::shared_ptr<CSGProducts>& products, bool showedges = false,
                         const RendererUtils::ShaderInfo *shaderinfo = nullptr,
                         bool highlight_mode = false, bool background_mode = false,
                         bool fberror = false) const;

  void createCSGProducts(const CSGProducts& products, VertexArray& vertex_array,
                         bool highlight_mode, bool background_mode);
  void createChainObject(VertexArray& vertex_array, const CSGChainObject& csgobj,
                         bool highlight_mode, bool background_mode,
                         OpenSCADOperator type);

  std::vector<std::shared_ptr<VertexState>> vertex_states_;
  std::shared_ptr<CSGProducts> root_products_;
  std::shared_ptr<CSGProducts> highlight_products_;
  std::shared_ptr<CSGProducts> background_products_;
  GLuint vertices_vbo_{0};
  GLuint elements_vbo_{0};
};
