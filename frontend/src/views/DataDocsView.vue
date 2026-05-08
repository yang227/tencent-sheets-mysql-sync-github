<template>
  <div class="docs-grid">
    <section class="panel docs-hero">
      <div>
        <h2>腾讯表格与 MySQL 数据同步实施说明</h2>
        <p class="section-copy">
          本页面用于说明平台的标准使用方式、实施顺序、运行边界与日常运维要求。
          建议按照“环境准备、连接配置、任务建模、试运行验证、正式运行、巡检维护”的顺序使用本系统，
          避免在凭证、表结构或字段映射未确认完成前直接进入持续同步。
        </p>
        <div class="tag-row" style="margin-top: 16px;">
          <span class="doc-tag">实施文档</span>
          <span class="doc-tag">配置规范</span>
          <span class="doc-tag">任务建模</span>
          <span class="doc-tag">运行巡检</span>
        </div>
      </div>

      <div class="docs-highlight">
        <div class="highlight-card">
          <strong>访问入口</strong>
          <div class="section-copy">平台首页 `/`，健康检查 `/health`，接口文档 `/docs`。</div>
        </div>
        <div class="highlight-card">
          <strong>最小运行条件</strong>
          <div class="section-copy">元数据库可连接，腾讯凭证有效，目标 MySQL 库表已准备完成。</div>
        </div>
        <div class="highlight-card">
          <strong>推荐部署方式</strong>
          <div class="section-copy">优先使用 Docker 统一启动服务，降低环境差异带来的排查成本。</div>
        </div>
      </div>
    </section>

    <section class="two-col-grid">
      <div class="panel">
        <h3 class="section-title">一、适用范围</h3>
        <ul class="bullet-list" style="margin-top: 14px;">
          <li>适用于腾讯在线表格与 MySQL 之间的表级数据同步。</li>
          <li>适用于需要可视化维护连接、映射、任务与运行状态的场景。</li>
          <li>适用于试运行、小规模生产和持续轮询同步场景。</li>
          <li>不建议在字段规则尚未稳定时直接用于高频关键主数据链路。</li>
        </ul>
      </div>

      <div class="panel">
        <h3 class="section-title">二、系统组成</h3>
        <div class="table-like" style="margin-top: 14px;">
          <div class="table-row">
            <strong>连接中心</strong>
            <span class="section-copy">维护 MySQL 连接与腾讯接口凭证，是所有同步任务的前置条件。</span>
          </div>
          <div class="table-row">
            <strong>同步任务</strong>
            <span class="section-copy">定义表格对象、目标表、同步方向、轮询频率及字段映射。</span>
          </div>
          <div class="table-row">
            <strong>运行监控</strong>
            <span class="section-copy">查看健康状态、执行结果、错误信息与整体吞吐情况。</span>
          </div>
          <div class="table-row">
            <strong>元数据库</strong>
            <span class="section-copy">保存平台配置、任务定义和运行日志，是后台管理能力的状态来源。</span>
          </div>
        </div>
      </div>
    </section>

    <section class="two-col-grid">
      <div class="panel">
        <h3 class="section-title">三、环境与配置要求</h3>
        <ul class="kv-list" style="margin-top: 14px;">
          <li><strong>config.yaml</strong>：定义平台监听地址、端口及元数据库基础配置。</li>
          <li><strong>.env</strong>：定义 Docker 场景下的容器参数、密码、凭证和加密密钥。</li>
          <li><strong>TENCENT_APP_ID / OPEN_ID / ACCESS_TOKEN</strong>：用于访问腾讯表格接口。</li>
          <li><strong>DATABASE_HOST / PORT / USER / PASSWORD</strong>：平台元数据库连接信息。</li>
          <li><strong>ENCRYPTION_KEY</strong>：敏感配置保护密钥，上线前必须替换默认占位值。</li>
        </ul>
      </div>

      <div class="panel">
        <h3 class="section-title">四、目标数据准备要求</h3>
        <ul class="bullet-list" style="margin-top: 14px;">
          <li>目标表应明确主键或唯一业务键。</li>
          <li>字段类型、长度、是否可空应在同步前确定。</li>
          <li>金额、日期、状态类字段建议先在数据库侧标准化。</li>
          <li>若表格字段经常变化，应建立变更审批或通知机制。</li>
          <li>首次接入建议从结构清晰、数据量较小的表开始验证。</li>
        </ul>
      </div>
    </section>

    <section class="panel">
      <h3 class="section-title">五、标准实施流程</h3>
      <div class="step-list" style="margin-top: 16px;">
        <div class="step-card">
          <span class="step-index">1</span>
          <div class="step-title">启动平台并确认基础健康状态</div>
          <div class="step-copy">
            建议执行 `docker compose up -d --build`，随后检查 `/health` 是否返回 healthy。
          </div>
        </div>
        <div class="step-card">
          <span class="step-index">2</span>
          <div class="step-title">维护连接中心信息</div>
          <div class="step-copy">
            先录入业务 MySQL 连接，再录入腾讯凭证，并分别执行连接测试。
          </div>
        </div>
        <div class="step-card">
          <span class="step-index">3</span>
          <div class="step-title">创建同步任务</div>
          <div class="step-copy">
            填写 Spreadsheet ID、Sheet ID、目标数据库、目标表、同步方向和轮询频率。
          </div>
        </div>
        <div class="step-card">
          <span class="step-index">4</span>
          <div class="step-title">读取字段并完成映射确认</div>
          <div class="step-copy">
            先读取腾讯字段和 MySQL 字段，再执行自动映射，并人工复核主键、金额、日期等关键字段。
          </div>
        </div>
        <div class="step-card">
          <span class="step-index">5</span>
          <div class="step-title">执行首轮试运行</div>
          <div class="step-copy">
            首次上线不要直接依赖定时轮询，应先手动触发一次，同步后核对数据行数、主键唯一性和异常日志。
          </div>
        </div>
        <div class="step-card">
          <span class="step-index">6</span>
          <div class="step-title">转入持续运行</div>
          <div class="step-copy">
            通过监控页持续观察成功率、失败次数、错误趋势和最近运行记录，确认链路稳定后再扩大使用范围。
          </div>
        </div>
      </div>
    </section>

    <section class="two-col-grid">
      <div class="panel">
        <h3 class="section-title">六、字段映射规范</h3>
        <ul class="bullet-list" style="margin-top: 14px;">
          <li>主键字段必须唯一且稳定，不建议使用随时会变的展示名作为主键。</li>
          <li>表格列名应尽量与数据库字段保持同一业务语义，减少自动映射偏差。</li>
          <li>新增字段时，先调整目标表结构，再补充任务映射，最后执行验证同步。</li>
          <li>对状态类、枚举类字段，应约束固定值集合，避免表格自由录入造成脏数据。</li>
          <li>跨系统时间字段应统一时区和格式，避免出现覆盖错误或重复同步。</li>
        </ul>
      </div>

      <div class="panel">
        <h3 class="section-title">七、运行巡检要求</h3>
        <ul class="bullet-list" style="margin-top: 14px;">
          <li>每日检查最近同步记录，确认没有连续失败任务。</li>
          <li>重点关注监控页中的错误数、失败数和整体健康状态。</li>
          <li>修改腾讯凭证或数据库密码后，必须重新执行连接测试。</li>
          <li>变更目标表结构后，必须重新读取 MySQL 字段并复核映射。</li>
          <li>上线初期建议缩短轮询周期并加强人工核对，稳定后再调整频率。</li>
        </ul>
      </div>
    </section>

    <section class="panel">
      <h3 class="section-title">八、常见问题与处理建议</h3>
      <div class="stack-list" style="margin-top: 16px;">
        <div class="stack-card">
          <div class="step-title">管理页能打开，但配置列表为空</div>
          <div class="step-copy">优先检查平台元数据库是否可连；元数据库异常时，后台接口通常无法返回配置数据。</div>
        </div>
        <div class="stack-card">
          <div class="step-title">自动映射结果不准确</div>
          <div class="step-copy">优先统一表头命名与数据库字段命名，再手动修正关键字段映射。</div>
        </div>
        <div class="stack-card">
          <div class="step-title">任务执行失败</div>
          <div class="step-copy">先查看运行监控中的最新错误，再区分凭证、表结构、网络或数据质量问题。</div>
        </div>
        <div class="stack-card">
          <div class="step-title">前端页面刷新后返回 404</div>
          <div class="step-copy">当前版本已补齐 SPA 路由兜底，业务页面和文档页均支持直接刷新访问。</div>
        </div>
      </div>
    </section>
  </div>
</template>
