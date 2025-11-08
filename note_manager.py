import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum
from config import config
import os

class RepeatType(Enum):
    """重复类型枚举"""
    NONE = "不重复"
    DAILY = "每天"
    WEEKDAYS = "每个工作日"
    WEEKLY = "每周"
    MONTHLY = "每月"
    YEARLY = "每年"

class Note:
    """笔记数据类"""
    def __init__(self, 
                 content: str = "",
                 due_date: Optional[datetime] = None,
                 repeat_type: RepeatType = RepeatType.NONE,
                 note_id: Optional[int] = None,
                 created_at: Optional[datetime] = None,
                 is_completed: bool = False):
        
        self.id = note_id
        self.content = content
        self.due_date = due_date or datetime.now().replace(second=0, microsecond=0)
        self.repeat_type = repeat_type
        self.created_at = created_at or datetime.now()
        self.is_completed = is_completed
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典用于序列化"""
        return {
            'id': self.id,
            'content': self.content,
            'due_date': self.due_date.isoformat(),
            'repeat_type': self.repeat_type.value,
            'created_at': self.created_at.isoformat(),
            'is_completed': self.is_completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Note':
        """从字典创建Note实例"""
        return cls(
            note_id=data['id'],
            content=data['content'],
            due_date=datetime.fromisoformat(data['due_date']),
            repeat_type=RepeatType(data['repeat_type']),
            created_at=datetime.fromisoformat(data['created_at']),
            is_completed=data['is_completed']
        )

class NoteManager:
    """笔记管理器"""
    
    def __init__(self):
        self.notes: List[Note] = []
        self._next_id = 1
        self.load_notes()
    
    def add_note(self, content: str, due_date: datetime, repeat_type: RepeatType) -> Note:
        """添加新笔记"""
        # 验证日期只能是今天或未来
        from datetime import datetime as PyDateTime
        if due_date.date() < PyDateTime.now().date():
            raise ValueError("只能记录今天和未来的事项")
        
        note = Note(
            content=content,
            due_date=due_date,
            repeat_type=repeat_type,
            note_id=self._next_id
        )
        
        self.notes.append(note)
        self._next_id += 1
        self.save_notes()
        return note
    
    def delete_note(self, note_id: int) -> bool:
        """删除笔记"""
        initial_length = len(self.notes)
        self.notes = [note for note in self.notes if note.id != note_id]
        
        if len(self.notes) != initial_length:
            self.save_notes()
            return True
        return False
    
    def mark_completed(self, note_id: int) -> bool:
        """标记笔记为完成"""
        for note in self.notes:
            if note.id == note_id:
                note.is_completed = True
                
                # 处理重复任务
                if note.repeat_type != RepeatType.NONE:
                    new_due_date = self._calculate_next_occurrence(
                        note.due_date, note.repeat_type
                    )
                    self.add_note(note.content, new_due_date, note.repeat_type)
                
                self.save_notes()
                return True
        return False
    
    def get_pending_notes(self) -> List[Note]:
        """获取待处理的笔记（今天和未来的未完成事项）"""
        now = datetime.now()
        pending_notes = []
        
        for note in self.notes:
            if not note.is_completed and note.due_date >= now:
                pending_notes.append(note)
        
        # 按时间排序
        pending_notes.sort(key=lambda x: x.due_date)
        return pending_notes
    
    def get_due_notes(self) -> List[Note]:
        """获取到期的笔记（需要提醒的）"""
        now = datetime.now()
        return [note for note in self.get_pending_notes() 
                if note.due_date <= now]
    
    def _calculate_next_occurrence(self, due_date: datetime, repeat_type: RepeatType) -> datetime:
        """计算下一次发生的时间"""
        if repeat_type == RepeatType.DAILY:
            return due_date + timedelta(days=1)
        elif repeat_type == RepeatType.WEEKDAYS:
            # 跳过周末
            next_date = due_date + timedelta(days=1)
            while next_date.weekday() >= 5:  # 5=周六, 6=周日
                next_date += timedelta(days=1)
            return next_date
        elif repeat_type == RepeatType.WEEKLY:
            return due_date + timedelta(weeks=1)
        elif repeat_type == RepeatType.MONTHLY:
            # 下个月的同一天
            year = due_date.year + (due_date.month // 12)
            month = due_date.month % 12 + 1
            try:
                return due_date.replace(year=year, month=month)
            except ValueError:
                # 如果下个月没有这一天，则取最后一天
                return due_date.replace(year=year, month=month, day=1) - timedelta(days=1)
        elif repeat_type == RepeatType.YEARLY:
            return due_date.replace(year=due_date.year + 1)
        else:
            return due_date
    
    def load_notes(self):
        """从文件加载笔记"""
        try:
            if not os.path.exists(config.notes_file_path):
                self.notes = []
                return
                
            with open(config.notes_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notes = [Note.from_dict(note_data) for note_data in data]
                
                # 更新下一个ID
                if self.notes:
                    self._next_id = max(note.id for note in self.notes) + 1
                    
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"加载笔记失败: {e}")
            self.notes = []
    
    def save_notes(self):
        """保存笔记到文件"""
        try:
            notes_data = [note.to_dict() for note in self.notes]
            with open(config.notes_file_path, 'w', encoding='utf-8') as f:
                json.dump(notes_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存笔记失败: {e}")

# 全局笔记管理器实例
note_manager = NoteManager()