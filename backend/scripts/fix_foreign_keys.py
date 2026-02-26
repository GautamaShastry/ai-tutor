"""
Fix foreign key constraints to reference learner_profiles instead of learners.
"""
import asyncio
from app.core.database import db


async def fix_foreign_keys():
    """Update foreign key constraints"""
    await db.connect()
    
    try:
        # Drop old foreign key constraints
        print("Dropping old foreign key constraints...")
        
        await db.execute("""
            ALTER TABLE learner_skills 
            DROP CONSTRAINT IF EXISTS learner_skills_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE spaced_repetition_items 
            DROP CONSTRAINT IF EXISTS spaced_repetition_items_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE placement_tests 
            DROP CONSTRAINT IF EXISTS placement_tests_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE error_memory 
            DROP CONSTRAINT IF EXISTS error_memory_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE lessons 
            DROP CONSTRAINT IF EXISTS lessons_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE chat_sessions 
            DROP CONSTRAINT IF EXISTS chat_sessions_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE sessions 
            DROP CONSTRAINT IF EXISTS sessions_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE learner_achievements 
            DROP CONSTRAINT IF EXISTS learner_achievements_learner_id_fkey;
        """)
        
        await db.execute("""
            ALTER TABLE pronunciation_attempts 
            DROP CONSTRAINT IF EXISTS pronunciation_attempts_learner_id_fkey;
        """)
        
        print("Creating new foreign key constraints...")
        
        # Add new foreign key constraints
        await db.execute("""
            ALTER TABLE learner_skills 
            ADD CONSTRAINT learner_skills_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE spaced_repetition_items 
            ADD CONSTRAINT spaced_repetition_items_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE placement_tests 
            ADD CONSTRAINT placement_tests_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE error_memory 
            ADD CONSTRAINT error_memory_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE lessons 
            ADD CONSTRAINT lessons_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE chat_sessions 
            ADD CONSTRAINT chat_sessions_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE sessions 
            ADD CONSTRAINT sessions_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE learner_achievements 
            ADD CONSTRAINT learner_achievements_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        await db.execute("""
            ALTER TABLE pronunciation_attempts 
            ADD CONSTRAINT pronunciation_attempts_learner_id_fkey 
            FOREIGN KEY (learner_id) REFERENCES learner_profiles(id) ON DELETE CASCADE;
        """)
        
        print("✓ Foreign key constraints fixed successfully!")
        
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(fix_foreign_keys())
