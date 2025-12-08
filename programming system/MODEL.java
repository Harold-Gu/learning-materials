// 如果有枚举类型，单独写在这里或者作为内部类
// public enum [枚举名] { TYPE_A, TYPE_B, TYPE_C }

public class [实体类名] {
    // 1. 私有属性 (根据题目要求列出)
    private String name;
    private [枚举名] type; 
    private int [数值属性1]; // 例如: age, temperature, price
    private int [数值属性2];

    // 2. 构造函数 (Constructor)
    public [实体类名](String name, [枚举名] type, int [数值属性1], int [数值属性2]) {
        // 调用验证逻辑
        validateInputs(name, [数值属性1], [数值属性2]);
        
        this.name = name;
        this.type = type;
        this.name = name;
        this.[数值属性1] = [数值属性1];
        this.[数值属性2] = [数值属性2];
    }

    // 3. 验证逻辑 (Task 1c 常考: 提取出来复用)
    private void validateInputs(String name, int val1, int val2) {
        // 验证名字长度
        if (name == null || name.length() < 3) {
            throw new IllegalArgumentException("Name must be at least 3 characters.");
        }
        // 验证数值范围 (例如: 0-100)
        if (val1 < 0 || val1 > 100) {
            throw new IllegalArgumentException("Value 1 is out of range.");
        }
        // 验证两个数值的关系 (例如: lower <= upper)
        if (val1 > val2) {
            throw new IllegalArgumentException("Value 1 cannot be greater than Value 2.");
        }
    }

    // 4. Getters and Setters (Setters 里也要加验证!)
    public String getName() { return name; }
    
    public void setName(String name) {
        if (name == null || name.length() < 3) throw new IllegalArgumentException("Invalid name");
        this.name = name;
    }

    public [枚举名] getType() { return type; }
    public void setType([枚举名] type) { this.type = type; }

    // ... 其他 getter/setter ...

    // 5. toString (方便打印)
    @Override
    public String toString() {
        return "[实体类名]{name='" + name + "', type=" + type + "}";
    }

    // 6. equals 和 hashCode (Task 1b 常考: 用于比较对象是否相同)
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        [实体类名] other = ([实体类名]) o;
        // 替换下面的比较逻辑 (通常比较 名字 和 类型)
        return this.type == other.type && this.name.equals(other.name);
    }

    @Override
    public int hashCode() {
        return java.util.Objects.hash(name, type);
    }
}



public class [容器类名] {
    // 1. 容器自身的属性
    private [枚举名] sizeLimit;  // 限制条件 (如: 最大承载尺寸)
    private int [环境属性];      // 环境条件 (如: 温度, 楼层)
    private int cost;           // 成本/价格 (用于 Task 3 比较)
    
    // 2. 当前居住者 (核心: Has-A 关系)
    private [实体类名] currentOccupant; // 如果能装多个，这里就是 List<实体>

    // 3. 构造函数 (初始化时通常为空)
    public [容器类名]([枚举名] sizeLimit, int [环境属性], int cost) {
        this.sizeLimit = sizeLimit;
        this.[环境属性] = [环境属性];
        this.cost = cost;
        this.currentOccupant = null; // 一开始是空的
    }

    // 4. Getters (通常容器属性是只读的，没有 Setters)
    public int getCost() { return cost; }
    public [实体类名] getOccupant() { return currentOccupant; }
    // ... 其他 getters ...

    // 5. 核心逻辑: 检查兼容性 (Task 2b 必考)
    public boolean checkCompatibility([实体类名] item) {
        if (item == null) return false;

        // 逻辑 A: 枚举比较 (例如: 物品尺寸 <= 容器尺寸)
        // 利用 ordinal() 比较大小: SMALL(0) < MEDIUM(1) < LARGE(2)
        boolean condition1 = item.getType().ordinal() <= this.sizeLimit.ordinal();

        // 逻辑 B: 数值范围比较 (例如: 容器温度在物品舒适范围内)
        // 假设 item 有 getMin() 和 getMax()
        boolean condition2 = this.[环境属性] >= item.getMin() && this.[环境属性] <= item.getMax();

        return condition1 && condition2;
    }

    // 6. 添加逻辑 (Task 2c)
    public void addItem([实体类名] item) {
        // 检查 1: 是否已经满了?
        if (this.currentOccupant != null) {
            throw new IllegalArgumentException("Container is already occupied.");
        }
        // 检查 2: 是否兼容?
        if (checkCompatibility(item)) {
            this.currentOccupant = item;
        } else {
            throw new IllegalArgumentException("Item is not compatible.");
        }
    }

    // 7. 移除逻辑
    public void removeItem() {
        this.currentOccupant = null; // 清空
    }
    
    @Override
    public String toString() {
        return "[容器类名] {Cost=" + cost + ", Occupant=" + currentOccupant + "}";
    }
}
















import java.util.ArrayList;
import java.util.List;

public class [管理类名] {
    // 1. 集合: 存放所有的容器
    private List<[容器类名]> containerList;

    public [管理类名]() {
        this.containerList = new ArrayList<>();
    }

    // 2. 添加容器
    public void addContainer([容器类名] c) {
        this.containerList.add(c);
    }

    // 3. 打印所有
    public void printAll() {
        for ([容器类名] c : containerList) {
            System.out.println(c);
        }
    }

    // 4. 核心难点: 智能分配 (Task 3c)
    // 目标: 找到一个合适的容器。如果有多个，选成本最低/空间最大的那个。
    public boolean allocate([实体类名] item) {
        [容器类名] bestMatch = null;

        for ([容器类名] c : containerList) {
            // 筛选条件 1: 容器必须是空的
            // 筛选条件 2: 容器必须兼容
            if (c.getOccupant() == null && c.checkCompatibility(item)) {
                
                // 优化条件: 选最好的 (例如: 成本最低)
                // 如果 bestMatch 还没找到，或者 当前 c 比 bestMatch 更便宜
                if (bestMatch == null || c.getCost() < bestMatch.getCost()) {
                    bestMatch = c;
                }
            }
        }

        // 找到了吗？
        if (bestMatch != null) {
            bestMatch.addItem(item); // 执行添加
            return true;
        }
        
        return false; // 没地方放
    }

    // 5. 查找并移除 (Task 3d)
    public void remove([实体类名] item) {
        boolean found = false;

        for ([容器类名] c : containerList) {
            // 检查容器里有没有东西，并且是不是我们要找的那个
            if (c.getOccupant() != null && c.getOccupant().equals(item)) {
                c.removeItem(); // 移除
                found = true;
                break; // 找到了就停止循环
            }
        }

        if (!found) {
            throw new IllegalArgumentException("Item not found in the system.");
        }
    }
}