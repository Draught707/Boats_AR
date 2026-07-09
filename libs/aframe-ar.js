AFRAME.registerComponent("ar-hit-test", {
  schema: {
    target: { type: "selector" }
  },

  init: function () {
    this.renderer = null;
    this.xrHitTestSource = null;
    this.refSpace = null;
    this.reticle = document.createElement("a-entity");
    this.reticle.setAttribute("geometry", {
      primitive: "ring",
      radiusInner: 0.06,
      radiusOuter: 0.08
    });
    this.reticle.setAttribute("material", {
      color: "#00ffff",
      shader: "flat",
      opacity: 0.8
    });
    this.reticle.setAttribute("rotation", "-90 0 0");
    this.reticle.setAttribute("visible", "false");
    this.el.appendChild(this.reticle);

    this.el.addEventListener("click", () => {
      if (this.reticle.object3D.visible && this.data.target) {
        const p = this.reticle.object3D.position;
        const q = this.reticle.object3D.quaternion;
        this.data.target.object3D.position.copy(p);
        this.data.target.object3D.quaternion.copy(q);
        this.data.target.setAttribute("visible", "true");
      }
    });

    this.el.sceneEl.addEventListener("enter-vr", () => {});
    this.el.sceneEl.renderer.xr.addEventListener("sessionstart", async () => {
      const sceneEl = this.el.sceneEl;
      if (!sceneEl.is("ar-mode")) return;

      this.renderer = sceneEl.renderer;
      const session = this.renderer.xr.getSession();
      const viewerSpace = await session.requestReferenceSpace("viewer");
      this.refSpace = this.renderer.xr.getReferenceSpace();
      this.xrHitTestSource = await session.requestHitTestSource({
        space: viewerSpace
      });
    });

    this.el.sceneEl.renderer.xr.addEventListener("sessionend", () => {
      this.xrHitTestSource = null;
      this.reticle.setAttribute("visible", "false");
    });
  },

  tick: function () {
    const sceneEl = this.el.sceneEl;
    const frame = sceneEl.frame;
    if (!frame || !this.xrHitTestSource || !this.refSpace) return;

    const hitTestResults = frame.getHitTestResults(this.xrHitTestSource);
    if (hitTestResults.length > 0) {
      const pose = hitTestResults[0].getPose(this.refSpace);
      if (pose) {
        this.reticle.object3D.visible = true;
        this.reticle.object3D.position.copy(pose.transform.position);
        this.reticle.object3D.quaternion.copy(pose.transform.orientation);
      }
    } else {
      this.reticle.object3D.visible = false;
    }
  }
});
